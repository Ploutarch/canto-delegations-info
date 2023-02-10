import os
import csv

print("Querying validators list...")
command = os.popen('cantod q staking validators')
full_validators = command.read()

only_val = full_validators.split("validators:")[1].split("\n- commission:")[1:]

val_addresses = []
for full_val in only_val:
    val_adr = [adr for adr in full_val.split(
        "\n") if "operator_address" in adr][0].strip().split("operator_address: ")[1]
    val_addresses.append(val_adr)

print("Finding all delegations...")
delegations = []
for adr in val_addresses:
    command = os.popen('cantod q staking delegations-to ' + adr)
    delegations_for_validator = command.read()
    only_del = delegations_for_validator.split("delegation_responses:")[
        1].split("\n- balance:")[1:]

    for dele in only_del:
        del_adr = [adr for adr in dele.split(
            "\n") if "delegator_address" in adr][0].strip().split("delegator_address: ")[1]
        amount = int([adr for adr in dele.split("\n") if "amount" in adr]
                     [0].strip().split("amount: ")[1].replace('"', ""))
        delegations.append([adr, del_adr, amount])

print("Writing to staking.csv...")
with open("staking.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Validator Address", "Delegator Address", "Tokens Staked"])
    writer.writerows(delegations)

print("Done!")

