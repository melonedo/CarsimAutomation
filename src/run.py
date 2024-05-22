from matlab.engine.matlabengine import MatlabEngine
import pywinauto, re, matlab.engine


class Automation:
    carsim: pywinauto.WindowSpecification
    simulink: pywinauto.WindowSpecification
    matlab: MatlabEngine

    def __init__(
        self,
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
        self.matlab = matlab.engine.connect_matlab() # type: ignore
        print(self.matlab)

    def send_to_simulink(self, silent=True):
        "Update configuration and send to simulink"
        if silent:
            self.carsim.send_keystrokes("%s")
        else:
            self.carsim.type_keys("%s")

    def run_simulink(self, slx="TVC_23b_SIL"):
        return self.matlab.sim(slx)

    def save_data(self, out, file):
        logsout = self.matlab.getfield(out, "logsout")
        self.matlab.exportToPreviousRelease(logsout, file, "data")

    def set_carsim_param(
        self,
        pars_file=r"C:\Users\melonedo\Documents\CarSim2019.1_Data\Procedures\Proc_39e0cbdf-b447-456e-b474-bb2dcd9cbb96.par",
        **kwargs,
    ):
        with open(pars_file, "rt") as f:
            pars = f.read()

        for k, v in kwargs.items():
            pars, n = re.subn(f"^({k}) (.+)$", f"\\1 {v}", pars, 0, re.MULTILINE)
            if not n:
                raise ValueError(f"Parameter {k} has no matches")
            if n > 1:
                raise ValueError(f"Parameter {k} has multiple matches")

        with open(pars_file, "wt") as f:
            f.write(pars)

a = Automation()
# a.send_to_simulink()
# a.run_simulink()
# a.set_carsim_param(SV_VXS=10)
out = a.run_simulink()
