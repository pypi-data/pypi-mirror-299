import base64
import json
from queue import Queue
from typing import Any, Literal
from urllib.parse import urlencode

import polars as pl
import requests

from quantplay.broker.generics.broker import Broker
from quantplay.model.broker import (
    MarginsResponse,
    ModifyOrderRequest,
    UserBrokerProfileResponse,
)
from quantplay.model.generics import (
    ExchangeType,
    OrderTypeType,
    ProductType,
    TransactionType,
)
from quantplay.model.order_event import OrderUpdateEvent

PROD_BASE_URL = "https://gw-napi.kotaksecurities.com/"
SESSION_PROD_BASE_URL = "https://napi.kotaksecurities.com/"


class Kotak(Broker):

    def __init__(
        self,
        order_updates: Queue[OrderUpdateEvent] | None = None,
        consumer_key: str | None = None,
        consumer_secret: str | None = None,
        mobilenumber: str | None = None,
        password: str | None = None,
        mpin: str | None = None,
        configuration: dict[str, str] | None = None,
        load_instrument: bool = True,
    ):
        super().__init__()

        self.configuration: dict[str, str] = {
            "fin_key": "X6Nk8cQhUgGmJ2vBdWw4sfzrz4L5En",
        }

        if configuration:
            self.configuration = {
                "fin_key": "X6Nk8cQhUgGmJ2vBdWw4sfzrz4L5En",
                "bearer_token": configuration["bearer_token"],
                "view_token": configuration["view_token"],
                "sid": configuration["sid"],
                "edit_token": configuration["edit_token"],
                "edit_sid": configuration["edit_sid"],
                "edit_rid": configuration["edit_rid"],
                "serverId": configuration["serverId"],
            }

        elif consumer_key and consumer_secret and mobilenumber and password and mpin:
            self.login(consumer_key, consumer_secret, mobilenumber, password, mpin)

    def login(
        self,
        consumer_key: str,
        consumer_secret: str,
        mobilenumber: str,
        password: str,
        mpin: str,
    ):
        base64_string = str(consumer_key) + ":" + str(consumer_secret)
        base64_token = base64_string.encode("ascii")

        base64_bytes = base64.b64encode(base64_token)
        final_base64_token = base64_bytes.decode("ascii")

        session_init = requests.post(
            url=f"{SESSION_PROD_BASE_URL}oauth2/token",
            headers={
                "Authorization": "Basic " + final_base64_token,
                "Content-Type": "application/json",
            },
            data=json.dumps({"grant_type": "client_credentials"}),
        )

        if not session_init.ok:
            raise Exception("")

        json_resp = json.loads(session_init.text)
        self.configuration["bearer_token"] = json_resp.get("access_token")

        view_token_resp = requests.post(
            url=f"{PROD_BASE_URL}login/1.0/login/v2/validate",
            headers={
                "Authorization": "Bearer " + self.configuration["bearer_token"],
                "Content-Type": "application/json",
            },
            data=json.dumps({"mobileNumber": mobilenumber, "password": password}),
        )
        view_token = json.loads(view_token_resp.text)

        self.configuration["view_token"] = view_token.get("data").get("token")
        self.configuration["sid"] = view_token.get("data").get("sid")

        view_token_resp = requests.post(
            url=f"{PROD_BASE_URL}login/1.0/login/v2/validate",
            headers={
                "Authorization": "Bearer " + self.configuration["bearer_token"],
                "sid": self.configuration["sid"],
                "Auth": self.configuration["view_token"],
                "Content-Type": "application/json",
            },
            data=json.dumps({"mobileNumber": mobilenumber, "password": password}),
        )

        login_resp = requests.post(
            url=f"{PROD_BASE_URL}login/1.0/login/v2/validate",
            headers={"Authorization": "Bearer " + self.configuration["bearer_token"]},
            data=json.dumps({"mobileNumber": mobilenumber, "mpin": mpin}),
        )
        edit_token_resp = json.loads(login_resp.text)

        if "error" not in edit_token_resp:
            self.configuration["edit_token"] = edit_token_resp.get("data").get("token")
            self.configuration["edit_sid"] = edit_token_resp.get("data").get("sid")
            self.configuration["edit_rid"] = edit_token_resp.get("data").get("rid")
            self.configuration["serverId"] = edit_token_resp.get("data").get("hsServerId")
            self.user_id = edit_token_resp.get("data").get("ucc")

        # decode_jwt = jwt.decode(  # type: ignore
        #     self.configuration["view_token"], options={"verify_signature": False}
        # )
        # userid = decode_jwt.get("sub")
        # self.kotakUserId = userid

        # generate_otp_resp = requests.post(
        #     url=f"{PROD_BASE_URL}login/1.0/login/otp/generate",
        #     headers={"Authorization": "Bearer " + self.configuration["bearer_token"]},
        #     data=json.dumps({"userId": userid, "sendEmail": True, "isWhitelisted": True}),
        # )

        # generate_otp = json.loads(generate_otp_resp.text)

    def get_base64_token(self, consumer_key: str, consumer_secret: str):
        """The Base64 Token Generation.
        This function will generate the Base64 Token this will be used to generate the Bearer Token.
        Return the Token in a String Format
        """

    # **
    # ** GET Api's
    # **

    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        orders_resp = self.request("order_book")

        if orders_resp["stat"] == "Not_Ok" and orders_resp["errMsg"] == "No Data":
            return pl.DataFrame(schema=self.orders_schema)
        orders_df = pl.DataFrame(orders_resp["data"])
        if "rejRsn" not in orders_df.columns:
            orders_df = orders_df.with_columns(pl.lit("").alias("rejRsn"))
        orders_df = orders_df.rename(
            {
                "actId": "user_id",
                "nOrdNo": "order_id",
                "exSeg": "exchange",
                "prod": "product",
                "trdSym": "tradingsymbol",
                "ordSt": "status",
                "prcTp": "order_type",
                "trnsTp": "transaction_type",
                "prc": "price",
                "avgPrc": "average_price",
                "trgPrc": "trigger_price",
                "ordDtTm": "order_timestamp",
                "tok": "token",
                "qty": "quantity",
                "fldQty": "filled_quantity",
                "rejRsn": "status_message",
            }
        )

        orders_df = orders_df.with_columns(
            pl.lit("regular").alias("variety"),
            pl.lit("").alias("tag"),
            pl.lit(None).alias("ltp"),
            pl.col("status_message").alias("status_message_raw"),
            pl.col("order_timestamp")
            .str.strptime(pl.Datetime(time_unit="ms"), format="%d-%b-%Y %H:%M:%S")
            .alias("order_timestamp"),
        )
        orders_df = orders_df.with_columns(
            pl.col("order_timestamp").alias("update_timestamp"),
            (pl.col("quantity") - pl.col("filled_quantity")).alias("pending_quantity"),
        )
        orders_df = orders_df[list(self.orders_schema.keys())].cast(self.orders_schema)

        orders_df = orders_df.with_columns(
            pl.when(pl.col("exchange") == "nse_cm")
            .then(pl.lit("NSE"))
            .when(pl.col("exchange") == "bse_cm")
            .then(pl.lit("BSE"))
            .when(pl.col("exchange") == "nse_fo")
            .then(pl.lit("NFO"))
            .when(pl.col("exchange") == "bse_fo")
            .then(pl.lit("BFO"))
            .when(pl.col("exchange") == "cde_fo")
            .then(pl.lit("CDS"))
            .when(pl.col("exchange") == "bcs-fo")
            .then(pl.lit("BCD"))
            .when(pl.col("exchange") == "mcx")
            .then(pl.lit("MCX"))
            .otherwise(pl.col("exchange"))
            .alias("exchange"),
            pl.when(pl.col("order_type") == "L")
            .then(pl.lit("LIMIT"))
            .when(pl.col("order_type") == "MKT")
            .then(pl.lit("MARKET"))
            .otherwise(pl.col("order_type"))
            .alias("order_type"),
            pl.when(pl.col("transaction_type") == "B")
            .then(pl.lit("BUY"))
            .when(pl.col("transaction_type") == "S")
            .then(pl.lit("SELL"))
            .otherwise(pl.col("transaction_type"))
            .alias("transaction_type"),
        )

        return orders_df

    def positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        positions_resp = self.request("order_book")

        if positions_resp["stat"] == "Not_Ok" and positions_resp["errMsg"] == "No Data":
            return pl.DataFrame(schema=self.positions_schema)

        return pl.DataFrame(schema=self.positions_schema)

    def holdings(self) -> pl.DataFrame:
        holdings_resp = self.request("order_book")

        if holdings_resp["stat"] == "Not_Ok" and holdings_resp["errMsg"] == "No Data":
            return pl.DataFrame(schema=self.holidings_schema)

        return pl.DataFrame(schema=self.holidings_schema)

    def ltp(self, exchange: ExchangeType, tradingsymbol: str) -> float:
        raise NotImplementedError()

    def profile(self) -> UserBrokerProfileResponse:
        return {"user_id": self.user_id or ""}

    def margins(self) -> MarginsResponse:
        limits_resp = self.request(
            "limits", body={"seg": "ALL", "exch": "ALL", "prod": "ALL"}
        )

        return {
            "margin_used": limits_resp["MarginUsed"],
            "margin_available": limits_resp["Net"],
            "total_balance": limits_resp["MarginUsed"] + limits_resp["Net"],
            "cash": 0,
        }

    # **
    # ** POST/PUT Api's
    # **

    def place_order(
        self,
        tradingsymbol: str,
        exchange: ExchangeType,
        quantity: int,
        order_type: OrderTypeType,
        transaction_type: TransactionType,
        tag: str | None,
        product: ProductType,
        price: float,
        trigger_price: float | None = None,
    ) -> str | None:
        place_order_body = {
            "am": "NO",
            "dq": "0",
            "es": self.get_exchange(exchange),
            "mp": "0",
            "pc": self.get_product(product),
            "pf": "N",
            "pr": str(price),
            "pt": self.get_order_type(order_type),
            "qt": str(quantity),
            "rt": "DAY",
            "tp": str(trigger_price or "0"),
            "ts": tradingsymbol,
            "tt": self.get_transaction_type(transaction_type),
            "ig": tag,
        }

        place_order_resp = self.request("place_order", body=place_order_body)
        print(place_order_resp)

        return ""

    def cancel_order(self, order_id: str, variety: str | None = None) -> None:
        return

    def modify_order(self, order: ModifyOrderRequest) -> str:
        return ""

    # **
    # ** General Utils
    # **

    def get_transaction_type(self, transaction_type: TransactionType) -> str:
        transaction_type_map: dict[TransactionType, str] = {
            "BUY": "B",
            "SELL": "S",
        }
        return transaction_type_map.get(transaction_type, transaction_type)

    def get_order_type(self, order_type: OrderTypeType) -> str:
        order_type_map: dict[OrderTypeType, str] = {
            "LIMIT": "L",
            "MARKET": "MKT",
            "SL": "SL",
            "SL-M": "SL-M",
        }

        return order_type_map.get(order_type, order_type)

    def get_exchange(self, exchange: ExchangeType) -> str:
        exchange_segment_map: dict[ExchangeType, str] = {
            "NSE": "nse_cm",
            "BSE": "bse_cm",
            "NFO": "nse_fo",
            "BFO": "bse_fo",
            "CDS": "cde_fo",
            "BCD": "bcs-fo",
            "MCX": "mcx",
        }

        return exchange_segment_map.get(exchange, exchange)

    def get_product(self, product: ProductType) -> str:
        product_map: dict[ProductType, str] = {
            "NRML": "NRML",
            "CNC": "CNC",
            "MIS": "MIS",
        }

        return product_map.get(product, product)

    # **
    # ** Kotak Utils
    # **

    def request(
        self,
        item: Literal[
            "place_order",
            "cancel_order",
            "modify_order",
            "order_history",
            "order_book",
            "trade_report",
            "positions",
            "holdings",
            "margin",
            "scrip_master",
            "limits",
            "logout",
        ],
        params: dict[str, str | int | float] | None = None,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url_map = {
            "place_order": ("Orders/2.0/quick/order/rule/ms/place", "POST", False),
            "cancel_order": ("Orders/2.0/quick/order/cancel", "POST", False),
            "modify_order": ("Orders/2.0/quick/order/vr/modify", "POST", False),
            "order_history": ("Orders/2.0/quick/order/history", "GET", True),
            "order_book": ("Orders/2.0/quick/user/orders", "GET", True),
            "trade_report": ("Orders/2.0/quick/user/trades", "GET", True),
            "positions": ("Orders/2.0/quick/user/positions", "GET", True),
            "holdings": ("Portfolio/1.0/portfolio/v1/holdings", "GET", True),
            "margin": ("Orders/2.0/quick/user/check-margin", "GET", True),
            "scrip_master": ("Files/1.0/masterscrip/v1/file-paths", "GET", True),
            "limits": ("Orders/2.0/quick/user/limits", "POST", False),
            "logout": ("login/1.0/logout", "GET", True),
        }

        url, method, is_content_type_json = url_map[item]
        content_type = (
            "application/json"
            if is_content_type_json
            else "application/x-www-form-urlencoded"
        )

        url = f"{PROD_BASE_URL}{url}"

        request_headers = {
            "Authorization": "Bearer " + self.configuration["bearer_token"],
            "Sid": self.configuration["edit_sid"],
            "Auth": self.configuration["edit_token"],
            "neo-fin-key": self.configuration["fin_key"],
            "Content-Type": content_type,
            "accept": "application/json",
        }

        query_params = {"sId": self.configuration["serverId"]}
        if item == "place_order":
            query_params["sId"] = "server4"
            request_headers["neo-fin-key"] = "neotradeapi"

        request_body = None
        request_params = None

        if params is not None:
            request_params = urlencode({**params, **query_params})
        else:
            request_params = urlencode(query_params)

        if body is not None:
            if content_type == "application/json":
                request_body = json.dumps(body)

            elif content_type == "application/x-www-form-urlencoded":
                request_body = {"jData": json.dumps(body)}

        resp = None
        resp_data = None

        if method == "GET":
            resp = requests.get(url=url, params=request_params, headers=request_headers)

        elif method == "POST":
            resp = requests.post(
                url=url,
                headers=request_headers,
                data=request_body,
                params=request_params,
            )

        if resp and resp.ok:
            resp_data = resp.json()

        if resp_data is None:
            raise Exception("")

        return resp_data
