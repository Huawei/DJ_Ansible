# -*- coding: UTF-8 -*-

import argparse
import csv
import datetime
import json
import os
import socket
import sys
import time

from util import httpclient

parser = argparse.ArgumentParser('generate_perf.sh')
parser.add_argument('-s', "--storage_ip",
                    help="The storage ip. "
                         "All storage will be query if it is not given.")
parser.add_argument('-b', "--begin", required=True,
                    type=lambda t: int(datetime.datetime.fromisoformat(
                        t).timestamp() * 1000),
                    help="Query start time. "
                         "Format: YYYY-MM-DD, example: 2000-01-01.")
parser.add_argument('-e', "--end",
                    type=lambda t: int(datetime.datetime.fromisoformat(
                        t).timestamp() * 1000 + 60 * 60 * 24 * 1000),
                    default=int(time.time() * 1000),
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
        "mode": {
            "mode_name": "specify_class",
            "mode_meta": {
                "class": "StorageName",
            }
        }
    },
    "Storage_IP": {
        "cn_title": "存储设备IP",
        "mode": {
            "mode_name": "specify_class",
            "mode_meta": {
                "class": "StorageIP",
            }
        }
    },
    "Storage_SN": {
        "cn_title": "存储设备SN",
        "mode": {
            "mode_name": "specify_class",
            "mode_meta": {
                "class": "StorageSN",
            }
        }
    },
    "Controller_CPU_Usage": {
        "cn_title": "控制器-CPU利用率（%）",
        "dataset": "perf-controller",
        "metric_name": "metrics.cpuUsage",
        "mode": {
            "mode_name": "max_avg_perf",
            "mode_meta": {
                "group_by": "dimensions.object.name"
            }
        }
    },
    "Controller_Read_IO_Response_Time": {
        "cn_title": "控制器-读I/O响应时间",
        "dataset": "perf-controller",
        "metric_name": "metrics.readResponseTime",
        "mode": {
            "mode_name": "max_avg_perf",
            "mode_meta": {
                "group_by": "dimensions.object.name"
            }
        }
    },
    "Controller_Write_IO_Response_Time": {
        "cn_title": "控制器-写I/O响应时间",
        "dataset": "perf-controller",
        "metric_name": "metrics.writeResponseTime",
        "mode": {
            "mode_name": "max_avg_perf",
            "mode_meta": {
                "group_by": "dimensions.object.name"
            }
        }
    },
    "Storage_Port_Usage": {
        "cn_title": "前端口-利用率（%）",
        "dataset": "perf-storage-port",
        "metric_name": "metrics.utility",
        "mode": {
            "mode_name": "max_avg_perf"
        }
    },
    "Storage_Port_Bandwidth": {
        "cn_title": "前端口-带宽",
        "dataset": "perf-storage-port",
        "metric_name": "metrics.bandwidth",
        "mode": {
            "mode_name": "max_avg_perf"
        }
    },
    "LUN_Read_IO_Response_Time": {
        "cn_title": "LUN-读I/O响应时间",
        "dataset": "perf-lun",
        "metric_name": "metrics.readResponseTime",
        "mode": {
            "mode_name": "max_avg_perf"
        }
    },
    "LUN_Write_IO_Response_Time": {
        "cn_title": "LUN-写I/O响应时间",
        "dataset": "perf-lun",
        "metric_name": "metrics.writeResponseTime",
        "mode": {
            "mode_name": "max_avg_perf"
        }
    },
    "Disk_Usage": {
        "cn_title": "硬盘-利用率（%）",
        "dataset": "perf-storage-disk",
        "metric_name": "metrics.utility",
        "mode": {
            "mode_name": "max_avg_perf"
        }
    },
    "FC_Replication_Link_IO_Response_Time": {
        "cn_title": "FC复制链路-IO响应时间",
        "dataset": "perf-remote-fclink",
        "metric_name": "metrics.avgIoResponseTime",
        "mode": {
            "mode_name": "max_avg_perf"
        }
    },
    "ISCSI_Replication_Link_IO_Response_Time": {
        "cn_title": "ISCSI复制链路-IO响应时间",
        "dataset": "perf-remote-iplink",
        "metric_name": "metrics.avgIoResponseTime",
        "mode": {
            "mode_name": "max_avg_perf"
        }
    },
    "TOP_5_Host_IOPS (AVG)": {
        "cn_title": "前五主机-IOPS (均值)",
        "dataset": "perf-storage-host",
        "metric_name": "metrics.throughput",
        "mode": {
            "mode_name": "top_perf",
            "mode_meta": {
                "top_order": "desc",
                "top_size": 5
            }
        }
    },
    "TOP_5_Host_Bandwidth (AVG)": {
        "cn_title": "前五主机-带宽 (均值)",
        "dataset": "perf-storage-host",
        "metric_name": "metrics.bandwidth",
        "mode": {
            "mode_name": "top_perf",
            "mode_meta": {
                "top_order": "desc",
                "top_size": 5
            }
        }
    },
    "TOP_5_Host_Read_IO_Latency (AVG)": {
        "cn_title": "前五主机-读IO时延 (均值)",
        "dataset": "perf-storage-host",
        "metric_name": "metrics.readTransDelay",
        "mode": {
            "mode_name": "top_perf",
            "mode_meta": {
                "top_order": "desc",
                "top_size": 5
            }
        }
    },
    "TOP_5_Host_Write_IO_Latency (AVG)": {
        "cn_title": "前五主机-写IO时延 (均值)",
        "dataset": "perf-storage-host",
        "metric_name": "metrics.writeTransDelay",
        "mode": {
            "mode_name": "top_perf",
            "mode_meta": {
                "top_order": "desc",
                "top_size": 5
            }
        }
    },
    "Storage_Capacity_Usage": {
        "cn_title": "存储空间使用率（%）",
        "dataset": "stat-storage-device",
        "metric_name": "metrics.capacityUsage",
        "mode": {
            "mode_name": "specify_class",
            "mode_meta": {
                "class": "StorageCapacity",
            }
        }
    }
}


class StorageCapacity:
    @staticmethod
    def get_value(storage):
        rules = [
            {
                "aggType": "avg",
                "aggRuleMeta": {
                    "field": "metrics.usedCapacity"
                },
                "ruleName": "usedCapacity"
            },
            {
                "aggType": "avg",
                "aggRuleMeta": {
                    "field": "metrics.usableCapacity"
                },
                "ruleName": "usableCapacity"
            }
        ]
        data = ESClient.request_es_dataset(
            "stat-storage-device", args.end - 60 * 60 * 24 * 1000,
            args.end,
            storage.get("pid"),
            rules,
            storage_id_field="dimensions.object.id").get("aggregations", {})
        used = data.get('usedCapacity').get("value")
        usable = data.get('usableCapacity').get("value")
        if not used or not usable:
            return

        return handle_value(used / usable * 100)


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
    def request_es_dataset(dataset, begin, end, stor_id, rules,
                           storage_id_field="dimensions.device.resId"):
        url = f'/rest/metrics/v1/datasets/{dataset}/statistics'
        raw_data = {
            "timeRange": {
                "endTime": end,
                "beginTime": begin,
                "granularity": "auto"
            },
            "aggs": {
                "rules": rules
            },
            "filters": {
                "dimensions": [
                    {
                        "field": storage_id_field,
                        "values": [stor_id]
                    }
                ]
            }
        }

        return request('post', url, raw_data)


def request(method, url, raw_data=None):
    code, resp = getattr(client, method)(url,
                                         raw_data) if \
        method != 'get' else getattr(client, method)(url)
    if code > 300:
        raise Exception(
            f"Request failed to {url} with {raw_data},"
            f" code: {code}, resp: {resp}")
    return json.loads(resp.decode())


class TitleManager:
    @staticmethod
    def get_title_key(metric):
        return metric[0] if not args.use_cn else metric[1].get('cn_title')


class ModeHistoryStatHandler:
    @staticmethod
    def get_metric_data(mode_meta, metric, stor, begin, end):
        metric_name, dataset = metric[1].get("metric_name"), metric[1].get(
            "dataset")
        rules = [
            {
                "aggType": "avg",
                "aggRuleMeta": {
                    "field": metric_name
                },
                "ruleName": "metrics_avg"
            }
        ]
        begin = end - 60 * 60 * 24 * 1000
        data = ESClient.request_es_dataset(dataset, begin, end,
                                           stor.get("pid"),
                                           rules).get('aggregations', {})
        return {TitleManager.get_title_key(metric): handle_value(
            data.get('metrics_avg', {}).get('value'))}

    @staticmethod
    def handle_title(tiles, metric):
        tiles.append(TitleManager.get_title_key(metric))


class ModeTopPerfHandler:
    @staticmethod
    def get_metric_data(mode_meta, metric, stor, begin, end):
        metric_name, dataset = metric[1].get("metric_name"), metric[1].get(
            "dataset")
        rules = [
            {
                "aggType": "groupby",
                "aggRuleMeta": {
                    "field": "dimensions.object.name",
                    "order": mode_meta.get("top_order",
                                           mode_meta.get("top_order", "desc")),
                    "orderKey": "avgRuleName",
                    "size": mode_meta.get("top_size",
                                          mode_meta.get("top_size", 5)),
                },
                "aggs": {
                    "rules": [{
                        "aggType": "avg",
                        "aggRuleMeta": {
                            "field": metric_name
                        },
                        "ruleName": "avgRuleName"
                    }]
                },
                "ruleName": "top_value"
            }
        ]

        data = ESClient.request_es_dataset(dataset, begin, end,
                                           stor.get("pid"),
                                           rules).get("aggregations", {})
        result = os.linesep.join([
            item.get("key") + ": " + handle_value(
                item.get("avgRuleName").get("value"))
            for item in
            data.get("top_value", {}).get("buckets", [])])

        return {TitleManager.get_title_key(metric): result}

    @staticmethod
    def handle_title(tiles, metric):
        tiles.append(TitleManager.get_title_key(metric))


class ModeMaxAvgPerfHandler:
    @classmethod
    def get_metric_data(cls, mode_meta, metric, stor, begin, end):
        metric_name, dataset = metric[1].get("metric_name"), metric[1].get(
            "dataset")

        if mode_meta.get("group_by"):
            max_value, avg_value = cls._get_data_with_group(dataset,
                                                            metric_name, stor,
                                                            begin, end,
                                                            mode_meta.get(
                                                                "group_by"))
        else:
            max_value, avg_value = cls._get_data(dataset, metric_name, stor,
                                                 begin, end)

        return {cls._get_max_title(metric): max_value,
                cls._get_avg_title(metric): avg_value}

    @staticmethod
    def _get_data(dataset, metric_name, stor, begin, end):
        rules = [
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
        data = ESClient.request_es_dataset(dataset, begin, end,
                                           stor.get("pid"),
                                           rules).get('aggregations', {})

        return handle_value(data.get('metrics_max', {}).get(
            'value')), handle_value(data.get('metrics_avg', {}).get('value'))

    @staticmethod
    def _get_data_with_group(dataset, metric_name, stor, begin, end,
                             group_field="dimensions.object.name"):
        rules = [
            {
                "aggType": "groupby",
                "aggRuleMeta": {
                    "field": group_field,
                },
                "aggs": {
                    "rules": [{
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
                        }]
                },
                "ruleName": "group_max_avg_value"
            }
        ]
        data = ESClient.request_es_dataset(dataset, begin, end,
                                           stor.get("pid"),
                                           rules).get('aggregations', {})

        max_dict = {}
        avg_dict = {}
        keys = []
        for item in data.get("group_max_avg_value", {}).get("buckets", []):
            key = item.get("key")
            keys.append(key)
            max_dict.update(
                {key: item.get("metrics_max").get("value")})
            avg_dict.update(
                {key: item.get("metrics_avg").get("value")})

        keys.sort()
        max_value = os.linesep.join(
            [key + ": " + handle_value(max_dict.get(key)) for key in keys])
        avg_value = os.linesep.join(
            [key + ": " + handle_value(avg_dict.get(key)) for key in keys])

        return max_value, avg_value

    @staticmethod
    def _get_max_title(metric):
        title = TitleManager.get_title_key(metric)
        suffix = '（峰值）' if args.use_cn else ' (MAX)'
        return title + suffix

    @staticmethod
    def _get_avg_title(metric):
        title = TitleManager.get_title_key(metric)
        suffix = '（均值）' if args.use_cn else ' (AVG)'
        return title + suffix

    @classmethod
    def handle_title(cls, tiles, metric):
        tiles.append(cls._get_max_title(metric))
        tiles.append(cls._get_avg_title(metric))


class ModeSpecifyClassHandler:
    @staticmethod
    def get_metric_data(mode_meta, metric, stor, begin, end):
        value = getattr(sys.modules[__name__],
                        mode_meta.get(
                            'class')).get_value(stor)
        return {TitleManager.get_title_key(metric): handle_value(value)}

    @staticmethod
    def handle_title(tiles, metric):
        tiles.append(TitleManager.get_title_key(metric))


class ModeContext:
    MODE_MAP = {
        "top_perf": ModeTopPerfHandler,
        "specify_class": ModeSpecifyClassHandler,
        "max_avg_perf": ModeMaxAvgPerfHandler,
        "history_stat": ModeHistoryStatHandler
    }

    @classmethod
    def get_mode_handler(cls, mode_name):
        return cls.MODE_MAP.get(mode_name)


def handle_value(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, float):
        return str('%.2f' % value)
    elif value is None:
        return ""
    else:
        return str(value)


def get_metric_data(stor, metric, begin, end):
    mode = metric[1].get("mode")
    mode_handler = ModeContext.get_mode_handler(mode.get("mode_name"))
    return mode_handler.get_metric_data(mode.get("mode_meta", {}), metric,
                                        stor, begin, end)


def get_storage_perf_data(stor):
    storage_perf = {}
    for metric in METRICS.items():
        storage_perf.update(
            get_metric_data(stor, metric, args.begin, args.end))
    return storage_perf


def get_perf_data():
    storages = get_storage_list()
    perf_datas = []
    for stor in storages:
        perf_datas.append(get_storage_perf_data(stor))
    return perf_datas


def get_storage_list():
    storages = request('get', '/rest/storagemgmt/v1/storages').get('datas')
    if args.storage_ip:
        return [stor for stor in storages if
                stor.get('ip') == args.storage_ip]
    return storages


def generate_report():
    perf_datas = get_perf_data()
    write_data(perf_datas)


def _get_csv_fieldnames():
    fieldnames = []
    for metric in METRICS.items():
        mode = metric[1].get("mode")
        mode_handler = ModeContext.get_mode_handler(mode.get("mode_name"))
        mode_handler.handle_title(fieldnames, metric)
    return fieldnames


def write_data(perf_datas):
    if not perf_datas:
        print("Empty perf data to write, return.")

    with open(DST_FILE_NAME, 'w', newline='',
              encoding='utf-8-sig') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=_get_csv_fieldnames())
        csv_writer.writeheader()
        csv_writer.writerows(perf_datas)


if __name__ == '__main__':
    generate_report()
    print(f'Successfully export data to file {DST_FILE_NAME}.')
