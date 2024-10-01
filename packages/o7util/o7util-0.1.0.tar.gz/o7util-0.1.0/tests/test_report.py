import o7util.report as o7report

# coverage run -m unittest -v tests.test_report && coverage report && coverage html


class ReportFunctions:

    # ---------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------
    def test_basic(self, mockPrint):

        r = o7report.Report("TheReport", section_name="First Section")
        assert r.name == "TheReport"
        assert len(r.sections) == 1
        assert len(r.sections[0].tests) == 0
        assert r.sections[0].name == "First Section"

        r.add_result(o7report.Test(name="Test OK", passed=True, critical=True))
        assert len(r.sections[0].tests) == 1
        assert r.sections[0].passed == 1

        r.add_result(
            o7report.Test(
                name="Test Fail", reason="Funny Stuff", passed=False, critical=True
            )
        )
        assert len(r.sections[0].tests) == 2
        assert r.sections[0].failed == 1

        r.add_result(
            o7report.Test(
                name="Test Fail but not critical", passed=False, critical=False
            )
        )
        assert len(r.sections[0].tests) == 3
        assert r.sections[0].warning == 1

        r.add_section("Second Section")
        assert len(r.sections) == 2
        assert len(r.sections[1].tests) == 0

        assert r.in_progress is None
        r.add_test("Step by Step Test 1", False)
        assert r.in_progress is not None
        assert r.in_progress.critical is False

        r.test_pass()
        assert r.in_progress is None
        assert len(r.sections[1].tests) == 1

        r.add_test("Step by Step Test 2", True)
        assert r.in_progress is not None
        assert r.in_progress.critical is True

        r.test_fail("Wrong Id")
        assert r.in_progress is None
        assert len(r.sections[1].tests) == 2

        r.add_test("Step by Step Test 3", False)
        assert r.in_progress is not None
        assert r.in_progress.critical is False

        r.add_parameter(name="Param1", value="Value1")

        r.complete()
        assert len(r.sections[1].tests) == 3

        r.complete()

    # ---------------------------------------------------------------------------------------------
    #
    # ---------------------------------------------------------------------------------------------
    def test_with_no_section(self, mockprint):

        r = o7report.Report("TheReport with No section", printout=False)
        assert r.name == "TheReport with No section"
        assert len(r.sections) == 0
        assert len(r.parameters) == 0

        r.add_parameter(name="Region", value="Canada")
        assert len(r.parameters) == 1
        assert r.parameters[0].name == "Region"
        assert r.parameters[0].value == "Canada"

        r.add_parameter(name="City")
        assert len(r.parameters) == 2
        assert r.parameters[1].name == "City"
        assert r.parameters[1].value is None

        r.add_result(o7report.Test(name="Test OK", passed=True, critical=True))
        assert len(r.sections[0].tests) == 1
        assert r.sections[0].passed == 1

        r.add_test("Step by Step Test 1")
        r.add_test("Step by Step Test 2")
        r.add_section("Second Section")

        assert r.sections[0].failed == 2

        r.test_pass()
        r.test_fail()

        r.complete()

    def test_with_no_section_2(self, mockprint):

        r = o7report.Report("TheReport with No section", printout=True)
        r.complete()


class Section:

    def test_init(self):

        obj = o7report.Section(
            "Section 1",
            tests=[o7report.Test(name="Test OK", passed=True, critical=True)],
        )
        assert obj.name == "Section 1"


def test_main(mocker):
    """Test main function"""

    mocker.patch.object(o7report, "__name__", new="__main__")
    o7report.main()
