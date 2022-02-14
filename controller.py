# -*- coding: utf-8 -*-

# python imports
import time
from math import degrees
import numpy as np
# pyfuzzy imports
from fuzzy.storage.fcl.Reader import Reader


class FuzzyController:

    def __init__(self, fcl_path):
        self.system = Reader().load_from_file(fcl_path)

    def _make_input(self, world):
        return dict(
            cp=world.x,
            cv=world.v,
            pa=degrees(world.theta),
            pv=degrees(world.omega)
        )

    def _make_output(self):
        return dict(
            force=0.
        )

    #def decide(self, world):
    #    output = self._make_output()
    #    print(self._make_input(world))
    #    self.system.calculate(self._make_input(world), output)
    #    return output['force']

    def calculate_result(self, crisp_input):
        # create fuzzy sets & calculate each sets memberships(fuzzification step)
        pa = dict()
        pv = dict()
        cp = dict()
        cv = dict()
        force = dict()
        pa["up_more_right"] = list()
        pa["up_more_right"] = [0.03, 0, -0.03, 2, 0, 0, 30, 1, 60, 0]
        pa["up_right"] = list()
        pa["up_right"] = [0.03, -1, -0.03, 3, 30, 0, 60, 1, 90, 0]
        pa["up"] = list()
        pa["up"] = [0.03, -2, -0.03, 4, 60, 0, 90, 1, 120, 0]
        pa["up_left"] = list()
        pa["up_left"] = [0.03, -3, -0.03, 5, 90, 0, 120, 1, 150, 0]
        pa["up_more_left"] = list()
        pa["up_more_left"] = [0.03, -4, -0.03, 6, 120, 0, 150, 1, 180, 0]
        pa["down_more_left"] = list()
        pa["down_more_left"] = [0.03, -6, -0.03, 8, 180, 0, 210, 1, 240, 0]
        pa["down_left"] = list()
        pa["down_left"] = [0.03, -7, -0.03, 9, 210, 0, 240, 1, 270, 0]
        pa["down"] = list()
        pa["down"] = [0.03, -8, -0.03, 10, 240, 0, 270, 1, 300, 0]
        pa["down_right"] = list()
        pa["down_right"] = [0.03, -9, -0.03, 11, 270, 0, 300, 1, 330, 0]
        pa["down_more_right"] = list()
        pa["down_more_right"] = [0.03, -10, -0.03, 12, 300, 0, 330, 1, 360, 0]
        pv["cw_fast"] = list()
        pv["cw_fast"] = [0, 1, -0.01, -1, -200, 1, -100, 0]
        pv["cw_slow"] = list()
        pv["cw_slow"] = [0.01, 2, -0.01, 0, -200, 0, -100, 1, 0, 0]
        pv["stop"] = list()
        pv["stop"] = [0.01, 1, -0.01, 1, -100, 0, 0, 1, 100, 0]
        pv["ccw_slow"] = list()
        pv["ccw_slow"] = [0.1, 0, -0.01, 2, 0, 0, 100, 1, 200, 0]
        pv["ccw_fast"] = list()
        pv["ccw_fast"] = [0.01, -1, 0, 1, 100, 0, 200, 1]
        cp["left_far"] = list()
        cp["left_far"] = [0, 1, -0.2, -1, -10, 1, -5, 0]
        cp["left_near"] = list()
        cp["left_near"] = [0.01, 1.33, -0.4, 0, -10, 0, -2.5, 1, 0, 0]
        cp["stop"] = list()
        cp["stop"] = [0.4, 1, -0.4, 1, -2.5, 0, 0, 1, 2.5, 0]
        cp["right_near"] = list()
        cp["right_near"] = [0.4, 0, -0.1, 1.33, 0, 0, 2.5, 1, 10, 0]
        cp["right_far"] = list()
        cp["right_far"] = [0.2, -1, 0, 1, 5, 0, 10, 1]
        cv["left_fast"] = list()
        cv["left_fast"] = [0, 1, -0.4, -1, -5, 1, -2.5, 0]
        cv["left_slow"] = list()
        cv["left_slow"] = [0.25, 1.25, -1, 0, -5, 0, -1, 1, 0, 0]
        cv["stop"] = list()
        cv["stop"] = [1, 1, -1, 1, -1, 0, 0, 1, 1, 0]
        cv["right_slow"] = list()
        cv["right_slow"] = [1, 0, -0.25, 1.25, 0, 0, 1, 1, 5, 0]
        cv["right_fast"] = list()
        cv["right_fast"] = [0.4, -1, 0, 1, 2.5, 0, 5, 1]
        force["left_fast"] = list()
        force["left_fast"] = [0.05, 5, -0.05, -3, -100, 0, -80, 1, -60, 0]
        force["left_slow"] = list()
        force["left_slow"] = [0.05, 4, -0.1, 0, -80, 0, -60, 1, 0, 0]
        force["stop"] = list()
        force["stop"] = [0.01, 1, -0.1, 1, -60, 0, 0, 1, 60, 0]
        force["right_slow"] = list()
        force["right_slow"] = [0.01, 0, -0.05, 4, 0, 0, 60, 1, 80, 0]
        force["right_fast"] = list()
        force["right_fast"] = [0.05, -3, -0.05, 5, 60, 0, 80, 1, 100, 0]
        pa_membership = dict()
        pv_membership = dict()
        cp_membership = dict()
        cv_membership = dict()
        force_membership = dict()

        for fuzzy_set in force:
            force_membership[fuzzy_set] = 0

        pa_input = crisp_input.get("pa")
        for fuzzy_set in pa:
            start = pa[fuzzy_set][4]
            end = pa[fuzzy_set][len(pa[fuzzy_set]) - 2]
            if start <= pa_input <= end:
                if pa[fuzzy_set][0] != 0 and pa[fuzzy_set][2] != 0:
                    if pa_input <= pa[fuzzy_set][6]:
                        pa_membership[fuzzy_set] = pa[fuzzy_set][0] * pa_input + pa[fuzzy_set][1]
                    else:
                        pa_membership[fuzzy_set] = pa[fuzzy_set][2] * pa_input + pa[fuzzy_set][3]
                else:
                    pa_membership[fuzzy_set] = pa[fuzzy_set][2] * pa_input + pa[fuzzy_set][3]
            else:
                pa_membership[fuzzy_set] = 0

        pv_input = crisp_input.get("pv")
        for fuzzy_set in pv:
            start = pv[fuzzy_set][4]
            end = pv[fuzzy_set][len(pv[fuzzy_set]) - 2]
            if start <= pv_input <= end:
                if pv[fuzzy_set][0] != 0 and pv[fuzzy_set][2] != 0:
                    if pv_input <= pv[fuzzy_set][6]:
                        pv_membership[fuzzy_set] = pv[fuzzy_set][0] * pv_input + pv[fuzzy_set][1]
                    else:
                        pv_membership[fuzzy_set] = pv[fuzzy_set][2] * pv_input + pv[fuzzy_set][3]
                else:
                    pv_membership[fuzzy_set] = pv[fuzzy_set][2] * pv_input + pv[fuzzy_set][3]
            else:
                pv_membership[fuzzy_set] = 0

        cp_input = crisp_input.get("cp")
        for fuzzy_set in cp:
            start = cp[fuzzy_set][4]
            end = cp[fuzzy_set][len(cp[fuzzy_set]) - 2]
            if start <= cp_input <= end:
                if cp[fuzzy_set][0] != 0 and cp[fuzzy_set][2] != 0:
                    if cp_input <= cp[fuzzy_set][6]:
                        cp_membership[fuzzy_set] = cp[fuzzy_set][0] * cp_input + cp[fuzzy_set][1]
                    else:
                        cp_membership[fuzzy_set] = cp[fuzzy_set][2] * cp_input + cp[fuzzy_set][3]
                else:
                    cp_membership[fuzzy_set] = cp[fuzzy_set][2] * cp_input + cp[fuzzy_set][3]
            else:
                cp_membership[fuzzy_set] = 0

        cv_input = crisp_input.get("cv")
        for fuzzy_set in cv:
            start = cv[fuzzy_set][4]
            end = cv[fuzzy_set][len(cv[fuzzy_set]) - 2]
            if start <= cv_input <= end:
                if cv[fuzzy_set][0] != 0 and cv[fuzzy_set][2] != 0:
                    if cv_input <= cv[fuzzy_set][6]:
                        cv_membership[fuzzy_set] = cv[fuzzy_set][0] * cv_input + cv[fuzzy_set][1]
                    else:
                        cv_membership[fuzzy_set] = cv[fuzzy_set][2] * cv_input + cv[fuzzy_set][3]
                else:
                    cv_membership[fuzzy_set] = cv[fuzzy_set][2] * cv_input + cv[fuzzy_set][3]
            else:
                cv_membership[fuzzy_set] = 0

        for fuzzy_set in pa_membership:
            if pa_membership[fuzzy_set] < 0:
                pa_membership[fuzzy_set] = 0
        for fuzzy_set in pv_membership:
            if pv_membership[fuzzy_set] < 0:
                pv_membership[fuzzy_set] = 0
        for fuzzy_set in cp_membership:
            if cp_membership[fuzzy_set] < 0:
                cp_membership[fuzzy_set] = 0
        for fuzzy_set in cv_membership:
            if cv_membership[fuzzy_set] < 0:
                cv_membership[fuzzy_set] = 0


        # inference step
        rules = dict()
        rules[0] = list()
        rules[0] = ["pa", "up", "and", "pv", "stop", "or", "pa", "up_right", "and", "pv", "ccw_slow", "or", "pa",
                    "up_left", "and", "pv", "cw_slow", "then", "force", "stop"]
        rules[1] = list()
        rules[1] = ["pa", "up_more_right", "and", "pv", "ccw_slow", "then", "force", "right_fast"]
        rules[2] = list()
        rules[2] = ["pa", "up_more_right", "and", "pv", "cw_slow", "then", "force", "right_fast"]
        rules[3] = list()
        rules[3] = ["pa", "up_more_left", "and", "pv", "cw_slow", "then", "force", "left_fast"]
        rules[4] = list()
        rules[4] = ["pa", "up_more_left", "and", "pv", "ccw_slow", "then", "force", "left_fast"]
        rules[5] = list()
        rules[5] = ["pa", "up_more_left", "and", "pv", "ccw_fast", "then", "force", "left_slow"]
        rules[6] = list()
        rules[6] = ["pa", "up_more_left", "and", "pv", "cw_fast", "then", "force", "right_fast"]
        rules[7] = list()
        rules[7] = ["pa", "up_more_left", "and", "pv", "cw_fast", "then", "force", "right_slow"]
        rules[8] = list()
        rules[8] = ["pa", "up_more_left", "and", "pv", "ccw_fast", "then", "force", "left_fast"]
        rules[9] = list()
        rules[9] = ["pa", "down_more_right", "and", "pv", "ccw_slow", "then", "force", "right_fast"]
        rules[10] = list()
        rules[10] = ["pa", "down_more_right", "and", "pv", "cw_slow", "then", "force", "stop"]
        rules[11] = list()
        rules[11] = ["pa", "up_more_left", "and", "pv", "cw_slow", "then", "force", "left_fast"]
        rules[12] = list()
        rules[12] = ["pa", "down_more_left", "and", "pv", "ccw_slow", "then", "force", "stop"]
        rules[13] = list()
        rules[13] = ["pa", "down_more_right", "and", "pv", "ccw_fast", "then", "force", "stop"]
        rules[14] = list()
        rules[14] = ["pa", "down_more_right", "and", "pv", "cw_fast", "then", "force", "stop"]
        rules[15] = list()
        rules[15] = ["pa", "down_more_left", "and", "pv", "cw_fast", "then", "force", "stop"]
        rules[16] = list()
        rules[16] = ["pa", "down_more_left", "and", "pv", "ccw_fast", "then", "force", "stop"]
        rules[17] = list()
        rules[17] = ["pa", "down_right", "and", "pv", "ccw_slow", "then", "force", "right_fast"]
        rules[18] = list()
        rules[18] = ["pa", "down_right", "and", "pv", "cw_slow", "then", "force", "right_fast"]
        rules[19] = list()
        rules[19] = ["pa", "down_left", "and", "pv", "cw_slow", "then", "force", "left_fast"]
        rules[20] = list()
        rules[20] = ["pa", "down_left", "and", "pv", "ccw_slow", "then", "force", "left_fast"]
        rules[21] = list()
        rules[21] = ["pa", "down_right", "and", "pv", "ccw_fast", "then", "force", "stop"]
        rules[22] = list()
        rules[22] = ["pa", "down_right", "and", "pv", "cw_fast", "then", "force", "right_slow"]
        rules[23] = list()
        rules[23] = ["pa", "down_left", "and", "pv", "cw_fast", "then", "force", "stop"]
        rules[23] = list()
        rules[24] = ["pa", "down_left", "and", "pv", "ccw_fast", "then", "force", "left_slow"]
        rules[25] = list()
        rules[25] = ["pa", "up_right", "and", "pv", "ccw_slow", "then", "force", "right_slow"]
        rules[26] = list()
        rules[26] = ["pa", "up_right", "and", "pv", "cw_slow", "then", "force", "right_fast"]
        rules[27] = list()
        rules[27] = ["pa", "up_right", "and", "pv", "stop", "then", "force", "right_fast"]
        rules[28] = list()
        rules[28] = ["pa", "up_left", "and", "pv", "cw_slow", "then", "force", "left_slow"]
        rules[29] = list()
        rules[29] = ["pa", "up_left", "and", "pv", "ccw_slow", "then", "force", "left_fast"]
        rules[30] = list()
        rules[30] = ["pa", "up_left", "and", "pv", "stop", "then", "force", "left_fast"]
        rules[31] = list()
        rules[31] = ["pa", "up_right", "and", "pv", "ccw_fast", "then", "force", "left_fast"]
        rules[32] = list()
        rules[32] = ["pa", "up_right", "and", "pv", "cw_fast", "then", "force", "right_fast"]
        rules[33] = list()
        rules[33] = ["pa", "up_left", "and", "pv", "cw_fast", "then", "force", "right_fast"]
        rules[34] = list()
        rules[34] = ["pa", "up_left", "and", "pv", "ccw_fast", "then", "force", "left_fast"]
        rules[35] = list()
        rules[35] = ["pa", "down", "and", "pv", "stop", "then", "force", "right_fast"]
        rules[36] = list()
        rules[36] = ["pa", "down", "and", "pv", "cw_fast", "then", "force", "stop"]
        rules[37] = list()
        rules[37] = ["pa", "down", "and", "pv", "ccw_fast", "then", "force", "stop"]
        rules[38] = list()
        rules[38] = ["pa", "up", "and", "pv", "ccw_slow", "then", "force", "left_slow"]
        rules[39] = list()
        rules[39] = ["pa", "up", "and", "pv", "ccw_fast", "then", "force", "left_fast"]
        rules[40] = list()
        rules[40] = ["pa", "up", "and", "pv", "cw_slow", "then", "force", "right_slow"]
        rules[41] = list()
        rules[41] = ["pa", "up", "and", "pv", "cw_fast", "then", "force", "right_fast"]
        rules[42] = list()
        rules[42] = ["pa", "up", "and", "pv", "stop", "then", "force", "stop"]
        # you could also add more rules with more input types
        res1 = 0
        res2 = 0
        res3 = 0
        f_res = 0
        result = 0
        res1 = min(pa_membership["up"], pv_membership["stop"])
        res2 = min(pa_membership["up_right"], pv_membership["ccw_slow"])
        res3 = min(pa_membership["up_left"], pv_membership["cw_slow"])
        f_res = max(res1, res2)
        result = max(f_res, res3)
        force_membership["stop"] = result
        c = 0
        for rule in rules:
            if c == 0:
                c = c + 1
                continue
            else:
                c = c + 1
            operation = ""
            result = 0
            for item in rules[rule]:
                if item == "pa":
                    index = rules[rule].index("pa") + 1
                    my_fuzzy_set = rules[rule][index]
                    if operation == "":
                        result = pa_membership[my_fuzzy_set]
                    else:
                        value = pa_membership[my_fuzzy_set]
                        if operation == "and":
                            result = min(result, value)
                        if operation == "or":
                            result = max(result, value)

                if item == "pv":
                    index = rules[rule].index("pv") + 1
                    my_fuzzy_set = rules[rule][index]
                    if operation == "":
                        result = pv_membership[my_fuzzy_set]
                    else:
                        value = pv_membership[my_fuzzy_set]
                        if operation == "and":
                            result = min(result, value)
                        if operation == "or":
                            result = max(result, value)

                if item == "cp":
                    index = rules[rule].index("cp") + 1
                    my_fuzzy_set = rules[rule][index]
                    if operation == "":
                        result = cp_membership[my_fuzzy_set]
                    else:
                        value = cp_membership[my_fuzzy_set]
                        if operation == "and":
                            result = min(result, value)
                        if operation == "or":
                            result = max(result, value)
                if item == "cv":
                    index = rules[rule].index("cv") + 1
                    my_fuzzy_set = rules[rule][index]
                    if operation == "":
                        result = cv_membership[my_fuzzy_set]
                    else:
                        value = cv_membership[my_fuzzy_set]
                        if operation == "and":
                            result = min(result, value)
                        if operation == "or":
                            result = max(result, value)
                if item == "and":
                    operation = "and"
                if item == "or":
                    operation = "or"
                if item == "then":
                    index = len(rules[rule]) - 1
                    my_fuzzy_set = rules[rule][index]
                    result = max(force_membership[my_fuzzy_set], result)
                    force_membership[my_fuzzy_set] = result



        # defuzzification
        new_force = dict()
        for fuzzy_set in force_membership:
            if force_membership[fuzzy_set] != 0:
                if force[fuzzy_set][0] == 0:
                    x1 = force[fuzzy_set][4]
                else:
                    x1 = (force_membership[fuzzy_set] - force[fuzzy_set][1])/force[fuzzy_set][0]
                if force[fuzzy_set][2] == 0:
                    x2 = force[fuzzy_set][len(force[fuzzy_set]) - 2]
                else:
                    x2 = (force_membership[fuzzy_set] - force[fuzzy_set][3])/force[fuzzy_set][2]
                new_force[fuzzy_set] = list()
                new_force[fuzzy_set].append(force[fuzzy_set][0])
                new_force[fuzzy_set].append(force[fuzzy_set][1])
                new_force[fuzzy_set].append(0)
                new_force[fuzzy_set].append(force_membership[fuzzy_set])
                new_force[fuzzy_set].append(force[fuzzy_set][2])
                new_force[fuzzy_set].append(force[fuzzy_set][3])
                new_force[fuzzy_set].append(force[fuzzy_set][4])
                new_force[fuzzy_set].append(force[fuzzy_set][5])
                new_force[fuzzy_set].append(x1)
                new_force[fuzzy_set].append(force_membership[fuzzy_set])
                new_force[fuzzy_set].append(x2)
                new_force[fuzzy_set].append(force_membership[fuzzy_set])
                new_force[fuzzy_set].append(force[fuzzy_set][8])
                new_force[fuzzy_set].append(force[fuzzy_set][9])
        points_of_force = np.linspace(-100, 100, 50)
        result = list()
        counter = 0
        for i in range(0, 50):
            result.append(0)

        non_zero_fuzzy_sets = list()
        for f_set in force_membership:
            if force_membership[f_set] != 0:
                non_zero_fuzzy_sets.append(f_set)

        for point in points_of_force:
            for fuzzy_set in non_zero_fuzzy_sets:
                if new_force[fuzzy_set][6] <= point <= new_force[fuzzy_set][8]:
                    res = new_force[fuzzy_set][0] * point + new_force[fuzzy_set][1]
                    if res > result[counter]:
                        result[counter] = res
                elif new_force[fuzzy_set][8] <= point <= new_force[fuzzy_set][10]:
                    res = new_force[fuzzy_set][2] * point + new_force[fuzzy_set][3]
                    if res > result[counter]:
                        result[counter] = res
                elif new_force[fuzzy_set][10] <= point <= new_force[fuzzy_set][12]:
                    res = new_force[fuzzy_set][4] * point + new_force[fuzzy_set][5]
                    if res > result[counter]:
                        result[counter] = res
            counter = counter + 1


        dx = points_of_force[1] - points_of_force[0]
        sum0 = 0
        sum1 = 0
        counter = 0
        for point in points_of_force:
            if result[counter] != 0:
                sum0 += result[counter]*point*dx
                sum1 += result[counter]*dx
            counter = counter + 1
        if sum0 != 0:
            return sum0/sum1
        else:
            return 0

    def decide(self, world):
        #output = self._make_output()
        #print(self._make_input(world))
        #self.system.calculate(self._make_input(world), output)
        force = self.calculate_result(self._make_input(world))
        return force
