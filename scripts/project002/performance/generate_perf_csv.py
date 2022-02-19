# -*- coding: UTF-8 -*-

import argparse
import csv
import datetime
import json
import socket
import sys
import time

from util import httpclient

parser = argparse.ArgumentParser('generate_perf.sh')
parser.add_argument('-s', "--storage_ip",
                    help="The storage ip. "
                         "All storage will be query if it is not given.")
parser.add_argument('-b', "--begin", required=True,
                    type=lambda t: datetime.datetime.fromisoformat(t),
                    help="Query start time. "
                         "Format: YYYY-MM-DD, example: 2000-01-01.")
parser.add_argument('-e', "--end",
                    type=lambda t: datetime.datetime.fromisoformat(t),
                    help="Query end time. "
                         "Format: YYYY-MM-DD, example: 2000-01-01.")
parser.add_argument("--use_cn", action='store_true',
                    help="Use chinese title. ")

args = parser.parse_args()

client = httpclient.CommonHttpClient(
    socket.gethostbyname(socket.gethostname()), 32018, True, False)

DST_FILE_NAME = 'perform_' + datetime.date.today().isoformat() + '.csv'

METRICS = {
    "Storage_Name": {
        "cn_title": "存储设备名称",
        "class": "StorageName",
        "is_performance": False
    },
    "Storage_IP": {
        "cn_title": "存储设备IP",
        "class": "StorageIP",
        "is_performance": False
    },
    "Storage_SN": {
        "cn_title": "存储设备SN",
        "class": "StorageSN",
        "is_performance": False
    },
    "Controller_CPU_Usage": {
        "cn_title": "控制器-CPU利用率（%）",
        "dataset": "perf-controller",
        "metric_name": "metrics.cpuUsage",
        "is_performance": True
    },
    "Controller_Read_IO_Response_Time": {
        "cn_title": "控制器-读I/O响应时间",
        "dataset": "perf-controller",
        "metric_name": "metrics.readResponseTime",
        "is_performance": True
    },
    "Controller_Write_IO_Response_Time": {
        "cn_title": "控制器-写I/O响应时间",
        "dataset": "perf-controller",
        "metric_name": "metrics.writeResponseTime",
        "is_performance": True
    },
    "Storage_Port_Usage": {
        "cn_title": "前端口-利用率（%）",
        "dataset": "perf-storage-port",
        "metric_name": "metrics.utility",
        "is_performance": True
    },
    "Storage_Port_Bandwidth": {
        "cn_title": "前端口-带宽",
        "dataset": "perf-storage-port",
        "metric_name": "metrics.bandwidth",
        "is_performance": True
    },
    "LUN_Read_IO_Response_Time": {
        "cn_title": "LUN-读I/O响应时间",
        "dataset": "perf-lun",
        "metric_name": "metrics.readResponseTime",
        "is_performance": True
    },
    "LUN_Write_IO_Response_Time": {
        "cn_title": "LUN-写I/O响应时间",
        "dataset": "perf-lun",
        "metric_name": "metrics.writeResponseTime",
        "is_performance": True
    },
    "Disk_Usage": {
        "cn_title": "硬盘-利用率（%）",
        "dataset": "perf-storage-disk",
        "metric_name": "metrics.utility",
        "is_performance": True
    },
    "FC_Replication_Link_IO_Response_Time": {
        "cn_title": "FC复制链路-IO响应时间",
        "dataset": "perf-remote-fclink",
        "metric_name": "metrics.avgIoResponseTime",
        "is_performance": True
    },
    "ISCSI_Replication_Link_IO_Response_Time": {
        "cn_title": "ISCSI复制链路-IO响应时间",
        "dataset": "perf-remote-iplink",
        "metric_name": "metrics.avgIoResponseTime",
        "is_performance": True
    },
    "Storage_Capacity_Usage": {
        "cn_title": "存储空间使用率（%）",
        "class": "StorageCapacity",
        "is_performance": False
    }
}


class StorageCapacity:
    @staticmethod
    def get_value(storage):
        return int(storage.get('used_capacity') / storage.get(
            'total_capacity') * 100)


class StorageName:
    @staticmethod
    def get_value(storage):
        return storage.get('name')


class StorageIP:
    @staticmethod
    def get_value(storage):
        return storage.get('ip')


class StorageSN:
    @staticmethod
    def get_value(storage):
        return storage.get('sn')


class ESClient:
    @staticmethod
    def get_dataset_statistic_value(stor_id, dataset, begin, end, metric_name):
        url = f'/rest/metrics/v1/datasets/{dataset}/statistics'
        raw_data = {
            "timeRange": {
                "endTime": end,
                "beginTime": begin,
                "granularity": "30min"
            },
            "aggs": {
                "rules": [
                    {
                        "aggType": "max",
                        "aggRuleMeta": {
                            "field": metric_name
                        },
                        "ruleName": "metrics_max"
                    },
                    {
                        "aggType": "avg",
                        "aggRuleMeta": {
                            "field": metric_name
                        },
                        "ruleName": "metrics_avg"
                    }
                ]
            },
            "filters": {
                "dimensions": [
                    {
                        "field": "dimensions.device.resId",
                        "values": [stor_id]
                    }
                ]
            }
        }
        data = request('post', url, raw_data)

        return data.get('aggregations').get('metrics_max').get(
            'value'), data.get('aggregations').get('metrics_avg').get('value')


def request(method, url, raw_data=None):
    code, resp = getattr(client, method)(url,
                                         raw_data) if \
        method != 'get' else getattr(client, method)(url)
    if code > 300:
        raise Exception(
            f"Request failed to {url} with {raw_data},"
            f" code: {code}, resp: {resp}")
    return json.loads(resp.decode())


def get_storage_list():
    storages = request('get', '/rest/storagemgmt/v1/storages').get('datas')
    if args.storage_ip:
        return [stor for stor in storages if
                stor.get('ip') == args.storage_ip]
    return storages


def get_metric_data(stor, metric_context, begin, end):
    return ESClient.get_dataset_statistic_value(stor.get('pid'),
                                                metric_context.get('dataset'),
                                                begin, end,
                                                metric_context.get(
                                                    'metric_name')) if \
        metric_context.get(
            'is_performance') else getattr(sys.modules[__name__],
                                           metric_context.get(
                                               'class')).get_value(stor)


def get_storage_perf_data(stor):
    begin = int(args.begin.timestamp() * 1000)
    end = int(args.end.timestamp() * 1000 + 60 * 60 * 24) if args.end else int(
        time.time() * 1000)
    storage_perf = {}
    for metric in METRICS.items():
        metric_title = metric[0]
        metric_context = metric[1]
        storage_perf.update({
            metric_title: get_metric_data(stor, metric_context,
                                          begin,
                                          end)})
    return storage_perf


def get_perf_data():
    storages = get_storage_list()
    perf_datas = []
    for stor in storages:
        perf_data = {}
        perf_data.update(get_storage_perf_data(stor))
        perf_datas.append(perf_data)
    return perf_datas


def generate_report():
    perf_datas = get_perf_data()
    write_data(perf_datas)


def _convert_perf_data(perf_data):
    converted_perf_data = {}
    for key, value in perf_data.items():
        if not isinstance(value, tuple):
            converted_perf_data.update({_get_title_key(key)[0]: value})
            continue
        else:
            converted_perf_data.update({
                _get_title_key(key)[0]: value[0],
                _get_title_key(key)[1]: value[1]
            })

    return converted_perf_data


def _get_title_key(key):
    config = METRICS.get(key)
    title = config.get('cn_title') if args.use_cn else key
    max_suffix = '（峰值）' if args.use_cn else ' (MAX)'
    avg_suffix = '（均值）' if args.use_cn else ' (AVG)'
    return (title + max_suffix, title + avg_suffix) if config.get(
        'is_performance') else (title,)


def _get_csv_fieldnames():
    fieldnames = []
    for key, value in METRICS.items():
        fieldnames.extend(_get_title_key(key))
    return fieldnames


def write_data(perf_datas):
    if not perf_datas:
        print("Empty perf data to write, return.")

    with open(DST_FILE_NAME, 'w', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=_get_csv_fieldnames())
        csv_writer.writeheader()
        csv_writer.writerows(list(map(_convert_perf_data, perf_datas)))


if __name__ == '__main__':
    generate_report()
    print(f'Successfully export data to file {DST_FILE_NAME}.')
