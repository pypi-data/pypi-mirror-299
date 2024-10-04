#!/usr/bin/env python3
"""Analize AVS metrology tests."""
import numpy as np
import matplotlib.pyplot as plt

try:
    import itkdb_gtk

except ImportError:
    import sys
    from pathlib import Path
    cwd = Path(__file__).parent.parent
    sys.path.append(cwd.as_posix())

from itkdb_gtk import ITkDBlogin, ITkDButils


def do_metrology(results, M_values):
    pass

def do_weighing(results, weights):
    """Accumulates weighing values to produce stack plot.

    Args:
        results (): Results from DB
        weights (): Dict with the values.
    """
    for value in results:
        ipos = value["code"].find("_")
        weights.setdefault(value["code"][ipos+1:], []).append(value["value"])


def plot_weighing(weights, tick_labels, show_total=False):
    """Make the plot of weights."""
    labels = ["COOLINGLOOPASSEMBLY", "LOCATOR_A", "LOCATOR_B", "LOCATOR_C", 
              "HONEYCOMBSET", "FACING_FRONT", "FACING_BACK", 
              "EPOXYADHESIVE", "EPOXYPUTTY", "EPOXYCONDUCTIVE"]

    fig = plt.figure(tight_layout=True)
    fig.suptitle("Petal Core weight (gr)")
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylabel("Weight [gr]")
    ax.set_ylim(0, 300)
    npoints = len(weights["CORE"])
    X = np.arange(npoints)

    values = [ weights[k] for k in labels]
    Y = np.vstack(values)
    ax.stackplot(X, Y, labels=labels)
    ax.set_xticks(range(npoints), labels=tick_labels, rotation="vertical")

    if not show_total:
        ax.plot(X, [225.0 for x in range(npoints)], linestyle="dashed", color="black", linewidth=1)
        ax.plot(X, [250.0 for x in range(npoints)], '-', color="black", linewidth=1, label="Nominal")
        ax.plot(X, [275.0 for x in range(npoints)], linestyle="dashed", color="black", linewidth=1,)


    ax.legend(loc="upper left", ncol=3, fontsize="x-small")


def main(session):
    """Entry point"""
    # find all cores
    # Now all the objects
    payload = {
        "filterMap": {
            "componentType": ["CORE_PETAL"],
            "type": ["CORE_AVS"],
            #"currentLocation": ["IFIC"],
        },
        "sorterList": [
            {"key": "alternativeIdentifier", "descending": False }
        ],
    }

    core_list = session.get("listComponents", json=payload)
    core_tests = ["METROLOGY_AVS", "WEIGHING"]

    weights = {}
    petal_ids = []
    M_values = []
    for core in core_list:
        SN = core["serialNumber"]
        altid = core['alternativeIdentifier']
        if "PPC" not in altid:
            continue

        if altid in ["PPC.016", "PPC.017"]:
            pass

        petal_ids.append(altid)

        location = core["currentLocation"]['code']
        coreStage = core["currentStage"]['code']

        print("\nPetal {} [{}] - {}. {}".format(SN, altid, coreStage, location))
        test_list = session.get("listTestRunsByComponent", json={"filterMap":{"serialNumber": SN, "state": "ready", "testType":core_tests}})

        good_tests = {}
        for tst in test_list:
            ttype = tst["testType"]["code"]
            if ttype not in core_tests:
                print(ttype)
                continue

            T = session.get("getTestRun", json={"testRun": tst["id"]})
            if T["state"] != "ready":
                continue

            print("-- {} [{}]".format(T["testType"]["name"], T["runNumber"]))
            if ttype in good_tests:
                if good_tests[ttype]["runNumber"] < T["runNumber"]:
                    good_tests[ttype] = T
            else:
                good_tests[ttype] = T

        for ttype, T in good_tests.items():

            if ttype == "WEIGHING":
                do_weighing(T["results"], weights)

            elif ttype == "METROLOGY_AVS":
                do_metrology(T["results"], M_values)
            
            else:
                for value in T["results"]:
                    print("\t{} - {}".format(value["code"], value["value"]))


                if not T["passed"]:
                    print("\t## test FAILED")

                print("\t+ Defects:")
                if len(T["defects"]):
                    for D in T["defects"]:
                        print("\t{} - {}".format(D["name"], D["description"]))
                else:
                    print("\nNone")

    plot_weighing(weights, petal_ids)
    plt.show()

if __name__ == "__main__":
    # ITk_PB authentication
    dlg = ITkDBlogin.ITkDBlogin()
    session = dlg.get_client()

    try:
        main(session)

    except Exception as E:
        print(E)

    dlg.die()