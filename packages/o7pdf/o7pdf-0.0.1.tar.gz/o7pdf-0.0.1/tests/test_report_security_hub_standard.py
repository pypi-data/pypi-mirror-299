import o7pdf.report_security_hub_standard as report
import o7util.pandas


def test_basic():

    dfs = o7util.pandas.dfs_from_excel("tests/sechub-data.xlsx")

    obj = report.ReportSecurityHubStandard(filename="cache/security_hub_standard.pdf")
    obj.generate(
        dfs=dfs, standard_arn="standards/cis-aws-foundations-benchmark/v/3.0.0"
    )
    obj.save()
