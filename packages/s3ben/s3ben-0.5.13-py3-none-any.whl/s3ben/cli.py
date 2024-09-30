import multiprocessing
import os
import pwd
from argparse import Namespace
from logging import getLogger

from s3ben.arguments import base_args
from s3ben.backup import BackupManager, ResolveRemmaping
from s3ben.config import parse_config
from s3ben.decorators import argument, command
from s3ben.logger import init_logger
from s3ben.rabbit import RabbitMQ
from s3ben.s3 import S3Events
from s3ben.sentry import init_sentry

_logger = getLogger(__name__)
args = base_args()
subparser = args.add_subparsers(dest="subcommand")


def main() -> None:
    """
    Entry point
    :raises ValueError: if config file not found
    :return: None
    """
    parsed_args = args.parse_args()
    if parsed_args.subcommand is None:
        args.print_help()
        return
    init_logger(name="s3ben", level=parsed_args.log_level)
    if os.path.isfile(parsed_args.sentry_conf):
        _logger.debug("Initializing sentry")
        init_sentry(config=parsed_args.sentry_conf)
    config = parse_config(parsed_args.config)
    parsed_args.func(config, parsed_args)


@command(parent=subparser)
def setup(config: dict, args: Namespace) -> None:
    """
    Cli command to add required cofiguration to s3 buckets and mq
    :param dict config: Parsed configuration dictionary
    :return: None
    """
    _logger.info("Checking backup root")
    main: dict = config.pop("s3ben")
    backup_root: str = main.pop("backup_root")
    user = pwd.getpwnam(main.pop("user"))
    if not os.path.exists(backup_root):
        os.mkdir(path=backup_root, mode=0o700)
        os.chown(path=backup_root, uid=user.pw_uid, gid=user.pw_gid)
    _logger.info("Setting up RabitMQ")
    mq_conf: dict = config.pop("amqp")
    exchange = mq_conf.pop("exchange")
    queue = mq_conf.pop("queue")
    routing_key = exchange
    mq_host = mq_conf.pop("host")
    mq_user = mq_conf.pop("user")
    mq_pass = mq_conf.pop("password")
    mq_port = mq_conf.pop("port")
    mq_virtualhost = mq_conf.pop("virtualhost")
    mq = RabbitMQ(
        hostname=mq_host,
        user=mq_user,
        password=mq_pass,
        port=mq_port,
        virtualhost=mq_virtualhost,
    )
    mq.prepare(exchange=exchange, queue=queue, routing_key=routing_key)
    _logger.info("Setting up S3")
    s3 = config.pop("s3")
    s3_events = S3Events(
        hostname=s3.pop("hostname"),
        access_key=s3.pop("access_key"),
        secret_key=s3.pop("secret_key"),
        secure=s3.pop("secure"),
    )
    all_buckets = s3_events.get_admin_buckets()
    exclude_buckets = s3.pop("exclude").split(",")
    exclude_buckets = [b.strip() for b in exclude_buckets]
    filtered_buckets = list(set(all_buckets) - set(exclude_buckets))
    s3_events.create_topic(
        mq_host=mq_host,
        mq_user=mq_user,
        mq_port=mq_port,
        mq_password=mq_pass,
        exchange=exchange,
        mq_virtualhost=mq_virtualhost,
    )
    for bucket in filtered_buckets:
        _logger.debug(f"Setting up bucket: {bucket}")
        s3_events.create_notification(bucket=bucket, exchange=exchange)


def init_consumer(config: dict) -> None:
    main = config.pop("s3ben")
    mq_conf: dict = config.pop("amqp")
    mq_host = mq_conf.pop("host")
    mq_user = mq_conf.pop("user")
    mq_pass = mq_conf.pop("password")
    mq_port = mq_conf.pop("port")
    queue = mq_conf.pop("queue")
    backup_root = main.pop("backup_root")
    s3 = config.pop("s3")
    s3_events = S3Events(
        hostname=s3.pop("hostname"),
        access_key=s3.pop("access_key"),
        secret_key=s3.pop("secret_key"),
        secure=s3.pop("secure"),
        backup_root=backup_root,
    )
    mq = RabbitMQ(
        hostname=mq_host,
        user=mq_user,
        password=mq_pass,
        port=mq_port,
        virtualhost=mq_conf.get("virtualhost"),
    )
    backup = BackupManager(
        backup_root=backup_root, user=main.pop("user"), mq=mq, mq_queue=queue
    )
    backup.start_consumer(s3_client=s3_events)


@command(parent=subparser)
def consume(config: dict, args: Namespace) -> None:
    s3ben_config: dict = config.get("s3ben")
    num_proc = s3ben_config.get("process") if "process" in s3ben_config.keys() else 8
    processes = []
    for _ in range(int(num_proc)):
        process = multiprocessing.Process(target=init_consumer, args=(config,))
        processes.append(process)
    for proc in processes:
        _logger.debug("Starting process: %s", proc)
        proc.start()
    for proc in processes:
        proc.join()


@command(
    [
        argument("--bucket", required=True, help="Bucket name which to sync", type=str),
        argument(
            "--transfers",
            help="Number of transfer processes, default: %(default)d",
            type=int,
            default=4,
        ),
        argument(
            "--checkers",
            help="Number of checker processes, default: %(default)d",
            type=int,
            default=4,
        ),
        argument("--skip-checksum", help="Skip checksum check", action="store_true"),
        argument("--skip-filesize", help="Skip filesize check", action="store_true"),
        argument(
            "--page-size",
            help="Bucket object page size, default: %(default)s",
            type=int,
            default=1000,
        ),
        argument(
            "--ui",
            help="Use experimental ui, default: %(default)s",
            action="store_true",
        ),
    ],
    parent=subparser,
)
def sync(config: dict, args: Namespace):
    """
    Entry point for sync cli option
    """
    _logger.debug("Initializing sync")
    s3 = config.pop("s3")
    backup_root = config["s3ben"].pop("backup_root")
    s3_events = S3Events(
        hostname=s3.pop("hostname"),
        access_key=s3.pop("access_key"),
        secret_key=s3.pop("secret_key"),
        secure=s3.pop("secure"),
        backup_root=backup_root,
    )
    backup = BackupManager(
        backup_root=backup_root,
        user=config["s3ben"].pop("user"),
        s3_client=s3_events,
        curses=args.ui,
    )
    backup.sync_bucket(
        args.bucket,
        args.transfers,
        args.page_size,
        args.checkers,
        args.skip_checksum,
        args.skip_filesize,
    )


@command(
    [
        argument("--show-excluded", help="Show excluded buckets", action="store_true"),
        argument("--show-obsolete", help="Show obsolete bucklets", action="store_true"),
        argument(
            "--only-enabled",
            help="Show only backup enabled buckets",
            action="store_true",
        ),
        argument(
            "--sort",
            help="Sort results by select collump, default: %(default)s",
            choices=["bucket", "owner", "size", "objects"],
            default="bucket",
        ),
        argument(
            "--sort-reverse", help="Reverse order for sorting", action="store_true"
        ),
    ],
    parent=subparser,
)
def buckets(config: dict, args: Namespace) -> None:
    _logger.debug("Listing buckets")
    s3 = config.pop("s3")
    exclude = s3.pop("exclude").replace('"', "").replace("'", "").split(",")
    exclude = [e.strip() for e in exclude]
    backup_root = config["s3ben"].pop("backup_root")
    s3_events = S3Events(
        hostname=s3.pop("hostname"),
        access_key=s3.pop("access_key"),
        secret_key=s3.pop("secret_key"),
        secure=s3.pop("secure"),
        backup_root=backup_root,
    )
    backup = BackupManager(
        backup_root=backup_root,
        user=config["s3ben"].pop("user"),
        s3_client=s3_events,
    )
    backup.list_buckets(
        exclude=exclude,
        show_excludes=args.show_excluded,
        show_obsolete=args.show_obsolete,
        only_enabled=args.only_enabled,
        sort=args.sort,
        sort_revers=args.sort_reverse,
    )


@command(
    [
        argument(
            "--days-keep",
            help="How long to keep, default: %(default)d",
            default=30,
            type=int,
        )
    ],
    parent=subparser,
)
def cleanup(config: dict, args: Namespace) -> None:
    """
    Cli function to call deleted items cleanup method
    from BackupManager
    """
    _logger.debug("Starting deleted items cleanup")
    backup_root = config["s3ben"].pop("backup_root")
    backup = BackupManager(
        backup_root=backup_root,
        user=config["s3ben"].pop("user"),
    )
    backup.cleanup_deleted_items(days=args.days_keep)
