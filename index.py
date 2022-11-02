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
user_delegations = {}
for adr in val_addresses:
    command = os.popen('cantod q staking delegations-to ' + adr)
    delegations = command.read()
    only_del = delegations.split("delegation_responses:")[
        1].split("\n- balance:")[1:]

    rew = 0
    for dele in only_del:
        indvidual_delegation = [adr for adr in dele.split(
            "\n") if "amount" in adr][0].strip().split("amount: ")[1]
        rew += int(indvidual_delegation.replace('"', ""))
        del_adr = [adr for adr in dele.split(
            "\n") if "delegator_address" in adr][0].strip().split("delegator_address: ")[1]
        amount = int([adr for adr in dele.split("\n") if "amount" in adr]
                     [0].strip().split("amount: ")[1].replace('"', ""))

        if del_adr in user_delegations:
            user_delegations[del_adr] += amount
        else:
            user_delegations[del_adr] = amount

print("Calculating total stake...")
evm_user_delegations = {}
for key in user_delegations.keys():
    command = os.popen('cantod debug addr ' + key)
    addresses = command.read()
    evm_address = [adr for adr in addresses.split(
        "\n") if "Address (EIP-55)" in adr][0].strip().split("Address (EIP-55): ")[1]

    evm_user_delegations[evm_address] = user_delegations[key]

print("Writing to staking.csv...")
with open("staking.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(list(evm_user_delegations.items()))

print("Done!")
