"""Module to handle api request"""
import requests
import spgci_qa.config
from .auth import get_token
from typing import Callable, Dict, Any, NamedTuple, Union
from pandas import DataFrame
import pandas as pd
from tqdm import tqdm
import warnings
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from .exceptions import AuthError, PerSecondLimitError, DailyLimitError
from time import sleep
from urllib.parse import urlparse, parse_qsl, urlencode, quote

_auth_retry = retry(
    retry=retry_if_exception_type(AuthError), reraise=True, stop=stop_after_attempt(2)
)
_throttle_retry = retry(
    retry=retry_if_exception_type(PerSecondLimitError), reraise=True, wait=wait_fixed(1)
)


class Paginator(NamedTuple):
    has_more_pages: bool
    key: str
    total_pages: int
    next_link: str = ""
    pg_type: str = ""


def _to_df(resp: requests.Response) -> DataFrame:
    j = resp.json()
    return DataFrame(j["results"])


def _paginate(resp: requests.Response) -> Paginator:
    return Paginator(False, "page", 1)


_session = requests.Session()


@_auth_retry
@_throttle_retry
def _get(
    url: str,
    params: Dict[Any, Any],
    session: requests.Session,
    include_auth_header: bool = True,
    # token_fn: Callable[[str, str, str, str], str] = get_token,
) -> requests.Response:
    headers = {
        "User-Agent": f"spgci-py/{spgci_qa.config.version}",
        # "Authorization": f"Bearer {token}",
        "appkey": spgci_qa.config.appkey,
    }

    if include_auth_header:
        token = get_token(
            spgci_qa.config.username,
            spgci_qa.config.password,
            spgci_qa.config.appkey,
            spgci_qa.config.base_url,
        )
        headers["Authorization"] = f"Bearer {token}"

    # should remove at some point..
    sleep(spgci_qa.config.sleep_time)

    response: requests.Response = session.get(
        url=url,
        params=params,
        headers=headers,
        verify=spgci_qa.config.verify_ssl,
        proxies=spgci_qa.config.proxies,
        auth=spgci_qa.config.auth,
    )

    # clear token cache and retry once if its a 401/403. shouldn't be hit unless token is expired..
    if response.status_code in [401, 403]:
        get_token.cache_clear()
        raise AuthError("Invalid Username, Password or Appkey")

    # if 429 check if more requests can be made today.
    if response.status_code == 429:
        rl = int(response.headers.get("x-ratelimit-remaining-day", 0))
        if rl > 0:
            raise PerSecondLimitError("Per Second Rate Limit Reached")
        else:
            raise DailyLimitError("Daily Rate Limit Reached")

    if response.status_code != 200:
        print(response.text)
        response.raise_for_status()

    return response


def get_data(
    path: str,
    params: Dict[Any, Any],
    df_fn: Callable[[requests.Response], DataFrame] = _to_df,
    paginate_fn: Callable[[requests.Response], Paginator] = _paginate,
    raw: bool = False,
    paginate: bool = False,
    include_auth_header: bool = True,
) -> Union[DataFrame, requests.Response]:
    url = f"{spgci_qa.config.base_url}/{path}"
    response = _get(
        url, params=params, include_auth_header=include_auth_header, session=_session
    )

    if raw:
        if paginate:
            warnings.warn(
                f"\nCannot set `paginate=True` along with `raw=True`. Returning only the page requested."
            )
        return response

    df: DataFrame = df_fn(response)
    pagination = paginate_fn(response)

    if not pagination.has_more_pages:
        return df

    if not paginate:
        warnings.warn(
            f"\nFetched page [1] of [{pagination.total_pages}]. set `paginate=True` to fetch all pages."
        )
        return df

    tp = pagination.total_pages
    if tp > 10:
        warnings.warn(
            f"\nWith `paginate=True` this will fetch {tp} pages. Set `paginate=False` to disable."
        )
    for i in tqdm(
        range(2, tp + 1),
        desc="Fetching...",
        initial=1,
        total=tp,
    ):
        # special handling for oData. Should refactor this at some point
        # also the pageSize param is hardcoded..
        if pagination.pg_type == "odata":
            parsed = urlparse(url)
            qs = dict(parse_qsl(parsed.query))
            qs[pagination.key] = str((i - 1) * int(qs["pageSize"]))
            parsed = parsed._replace(query=urlencode(qs, quote_via=quote))
            resp = _get(url=parsed.geturl(), params={}, session=_session)
        else:
            params[pagination.key] = i
            resp = _get(
                url,
                params=params,
                include_auth_header=include_auth_header,
                session=_session,
            )

        new_df = df_fn(resp)
        df: DataFrame = pd.concat(objs=[df, new_df], ignore_index=True)  # type: ignore

    return df
