# -*- coding: utf-8 -*-

import click
from tcfcli.help.message import EventHelp as help
from tcfcli.common.operation_msg import Operation
from tcfcli.libs.utils.scf_client import ScfClient
from tcfcli.common.user_exceptions import *
from tcfcli.common.user_config import UserConfig
import tcfcli.common.base_infor as infor

REGIONS = infor.REGIONS


class List(object):
    @staticmethod
    def do_cli(region, namespace, name):
        List.show(region, namespace, name)

    @staticmethod
    def show(region, namespace,name):
        if region and region not in REGIONS:
            raise ArgsException("region {r} not exists ,please select from{R}".format(r=region, R=REGIONS))
        if not region:
            region = UserConfig().region

        rep = ScfClient(region).get_ns(namespace)
        if not rep:
            raise NamespaceException("Region {r} not exist namespace {n}".format(r=region, n=namespace))

        functions = ScfClient(region).get_function(function_name=name, namespace=namespace)
        if not functions:
            raise FunctionNotFound("Region {r} namespace {n} not exist function {f}".format(r=region, n=namespace, f=name))
            return

        Operation("Region:%s" % (region)).process()
        Operation("Namespace:%s " % (namespace)).process()
        Operation("Function:%s " % (name)).process()
        testmodels = ScfClient(region).list_func_testmodel(functionName=name, namespace=namespace)
        if not testmodels:
            raise NamespaceException("This function not exist event".format(f=name))

        click.secho("%-20s %-20s %-20s" % ("TestmodelsName", "AddTime", "ModTime"))
        for testmodel in testmodels:
            res = ScfClient(region).get_func_testmodel(functionName=name, namespace=namespace, testModelName=testmodel)
            click.secho("%-20s %-20s %-20s" % (testmodel, res['CreatedTime'], res['ModifiedTime']))
        click.secho("\n")


@click.command(name='list', short_help=help.LIST_SHORT_HELP)
@click.option('--region', '-r', help=help.REGION)
@click.option('-ns', '--namespace', default="default", help=help.NAMESPACE)
@click.option('-n', '--name', required=True, help=help.FUNCTION_NAME_HELP)
def list(region, namespace, name):
    """
        \b
        Show the SCF event list.
        \b
        Common usage:
        \b
            * All function in ap-guangzhou
              $ scf event list --region ap-guangzhou --name test
    """
    List.do_cli(region, namespace, name)


