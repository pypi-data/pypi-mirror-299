import asyncio
import ssl
from threading import ExceptHookArgs
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import Envelope, Session, AuthResult, LoginPassword
import argparse
from pathlib import Path
import mailbox
import sys
import pudb
from email import message_from_bytes
from pydantic import BaseModel, validator


class MailServerArgs(BaseModel):
    mdir: str = "/tmp/mail"
    mbox: str = "messages.mbox"
    tls: bool = False
    port: int = 22225

    @validator("mdir", "mbox")
    def validate_path(cls, v):
        path = Path(v)
        if not path.is_dir():
            raise ValueError(f"{v} is not a valid directory path")
        return path


class Mbox365Handler:
    # async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
    #     pass
    # if not address.endswith("@example.com"):
    #     return "550 not relaying to that domain"
    # envelope.rcpt_tos.append(address)
    # return "250 OK"

    def __init__(self, mboxFile: Path):
        self.mboxFile: Path = mboxFile

    async def handle_DATA(
        self, server: Controller, session: Session, envelope: Envelope
    ):
        try:
            contents = envelope.content
            msg: str = message_from_bytes(contents)
            print(f"Message from {envelope.mail_from}")
            print(f"Message for {envelope.rcpt_tos}")
            print(f"Message data:\n{contents}")
            print("End of message")
            mbox: mailbox.mbox = mailbox.mbox(self.mboxFile, create=True)
            mbox.add(msg)
            mbox.flush()
            mbox.close()

            return "250 Message accepted for delivery"

        except Exception as e:
            # Handle unrecognized commands
            print(f"Unrecognized command or data received: {e}")
            return "500 Syntax error: command unrecognized"

    async def handle_AUTH(
        self, server: Controller, session: Session, envelope: Envelope, args: bytes
    ) -> AuthResult:
        pudb.set_trace()
        if args[0].decode() == "PLAIN":
            if args[1].decode() == "\x00ch137123@gmail.com\x00your_password":
                session.authenticated = True
                return AuthResult(success=True)
        return AuthResult(success=False)


def context_get() -> ssl.SSLContext:
    # Create SSL context without requiring encryption for TLS
    context: ssl.SSLContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("cert.pem", "key.pem")
    # Set options to allow plaintext connections
    # context.options |= ssl.OP_NO_TLSv1_3  # Disable TLS 1.3
    # context.options |= ssl.OP_NO_TLSv1_2  # Disable TLS 1.2
    # context.options |= ssl.OP_NO_TLSv1_1  # Disable TLS 1.1
    # context.options |= ssl.OP_NO_TLSv1  # Disable TLS 1.0
    # context.options |= ssl.OP_NO_SSLv3  # Disable SSL 3.0
    return context


def controller_get(args: MailServerArgs) -> Controller:
    auth_credentials = LoginPassword("ch137123@gmail.com", "your_password")
    controller: Controller
    if args.tls:
        controller = AuthController(
            Mbox365Handler(args.mdir / args.mbox),
            auth_credentials,
            port=args.port,
            ssl_context=context_get(),
        )
        print(f"TLS mailserver listening on {args.port}")
    else:
        controller = Controller(Mbox365Handler(args.mdir / args.mbox), port=args.port)
        print(f"No auth mailserver listening on {args.port}")

    return controller


def env_check(args: argparse.Namespace) -> bool:
    OK: bool = False
    mbox_path = Path(args.mdir) / Path(args.mbox)
    try:
        mbox_path.parent.mkdir(parents=True, exist_ok=True)
        OK = True
    except Exception as e:
        print(f"An error occured checking the env: {e}")

    print(f"All email will be sunk to {args.mdir}/{args.mbox}")
    return OK


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mail sink server")
    parser.add_argument(
        "--mdir",
        required=False,
        help="Output mbox directory",
        default="/tmp/mail",
        type=str,
    )
    parser.add_argument(
        "--mbox",
        required=False,
        help="Output mbox file",
        default="messages.mbox",
        type=str,
    )
    parser.add_argument(
        "--tls",
        required=False,
        help="toggle TLS context",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--port",
        required=False,
        help="Listener port",
        default=22225,
        type=int,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args: argparse.Namespace = parse_arguments()

    if not env_check(args):
        sys.exit(1)

    controller: Controller = controller_get(args)
    controller.start()
    input("Press enter to stop")
    controller.stop()
