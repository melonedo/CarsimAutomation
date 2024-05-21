import pywinauto, re


class Automation:
    carsim: pywinauto.WindowSpecification
    simulink: pywinauto.WindowSpecification
    pars_file: str

    def __init__(
        self,
        pars_file=r"C:\Users\melonedo\Documents\CarSim2019.1_Data\Procedures\Proc_39e0cbdf-b447-456e-b474-bb2dcd9cbb96.par",
        carsim_path=r"C:\Users\melonedo\AppData\Local\CarSim2019.1_Prog\CarSim.exe",
        matlab_path=r"C:\Program Files\MATLAB\R2023a\bin\win64\MATLAB.exe",
        simulink_re=r".* - Simulink academic use",
    ):
        self.carsim = pywinauto.Application().connect(path=carsim_path).top_window()
        self.simulink = (
            pywinauto.Application()
            .connect(path=matlab_path)
            .window(title_re=simulink_re)
        )
        self.pars_file = pars_file

    def send_to_simulink(self):
        # self.carsim.send_keystrokes("%s")
        self.carsim.type_keys("%s")

    def run_now(self):
        self.carsim.type_keys("%r")

    def run_simulink(self):
        self.simulink.type_keys("^t")

    def set_param(self, **kwargs):
        with open(self.pars_file, "rt") as f:
            pars = f.read()
        for k, v in kwargs.items():
            # print(f"^{k} (.+)$")
            # print(re.findall(f"^{k} (.+)$", pars, re.MULTILINE))
            pars, n = re.subn(f"^({k}) (.+)$", f"\\1 {v}", pars, 0, re.MULTILINE)
            if not n:
                raise ValueError(f"Parameter {k} has no matches")
            if n > 1:
                raise ValueError(f"Parameter {k} has multiple matches")

        with open(self.pars_file, "wt") as f:
            f.write(pars)


a = Automation()
# a.send_to_simulink()
# a.run_simulink()
a.set_param(SV_VXS=10)
