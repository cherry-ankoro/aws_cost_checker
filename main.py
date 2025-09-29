import boto3
import yaml
import os
import typing import Any, Dict, Optional

def load_config(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFountError(f"config is not found.")
    with open (path, "r", encording="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def create_boto3_session(cfg: Dict[str, Any]) -> boto3.session.Session:
    auth_mode: str = cfg.get("auth_mode") or "user"
    os.environ['AWS_ACCESS_KEY_ID'] = cfg.get("access_key")
    os.environ['AWS_SECRET_ACCESS_KEY'] = cfg.get("secret_key")
    os.environ['AWS_DEFAULT_REGION'] = cfg.get('region')

    if auth_mode == "user":
        pass
    elif auth_mode == "role":
        pass
    else:
        print("auth mode is undefined")

    return boto3.Session()


def get_cost_by_service(
    session: boto3.session.Session,
    time_period: Dict[str, str],
    granularity: str,
    metric: str = "UnblendedCost"
) -> List[Dict[str, Any]]:
    ce = session.client("ce")
    
    params: Dict[str, Any] = {
        "TimePeriod": time_period,
        "Granularity": granularity,
        "Metrics": [metric],
        "GroupBy": [{"Type": "DIMENSION", "Key": "SERVICE"}],
    }

    while True:
        if next_token:
            params["NextPageToken"] = next_token
        resp = ce.get_cost_and_usage(**params)
        results.extend(resp.get("ResultsByTime", []))
        next_token = resp.get("NextPageToken")
        if not next_token:
            break

    return results


def output_result(results: List[Dict[str, Any]]):
    """
    後でちゃんとした処理を書く
    """
    print(results)


def main():
    try:
        aws_cfg = load_config()
        cost_cfg = load_config()
        create_boto3_session()
        get_by_cost_service()
        ## 出力用関数を書く
    except Exception as e:
        sys.exit(1)


if __name__ == "__main__":
    main()
