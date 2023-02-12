import os
import csv

print("Querying validators list...")
command = os.popen('cantod q staking validators')
full_validators = command.read()

only_val = full_validators.split("validators:")[1].split("\n- commission:")[1:]

val_addresses = []
val_monikers = {}
for full_val in only_val:
    val_adr = [adr for adr in full_val.split("\n") if "operator_address" in adr][0].strip().split("operator_address: ")[1]
    val_moniker = [adr for adr in full_val.split("\n") if "description.moniker" in adr]
    if val_moniker:
        val_moniker = val_moniker[0].strip().split("description.moniker: ")[1]
    else:
        val_moniker = "Unknown Moniker"
    val_addresses.append(val_adr)
    val_monikers[val_adr] = val_moniker

print("Finding all delegations...")
delegations_list = []
for adr in val_addresses:
    command = os.popen('cantod q staking delegations-to ' + adr)
    delegations = command.read()
    only_del = delegations.split("delegation_responses:")[1].split("\n- balance:")[1:]

    for dele in only_del:
        val_address = adr
        del_adr = [adr for adr in dele.split("\n") if "delegator_address" in adr][0].strip().split("delegator_address: ")[1]
        amount = int([adr for adr in dele.split("\n") if "amount" in adr][0].strip().split("amount: ")[1].replace('"', ""))

        delegations_list.append([val_address, del_adr, amount])

print("Calculating total stake...")
evm_delegations_list = []
for delegation in delegations_list:
    val_address = delegation[0]
    del_adr = delegation[1]
    amount = delegation[2]

    command = os.popen('cantod debug addr ' + del_adr)
    addresses = command.read()
    evm_address = [adr for adr in addresses.split("\n") if "Address (EIP-55)" in adr][0].strip().split("Address (EIP-55): ")[1]

    evm_delegations_list.append([val_monikers[val_address], val_address, evm_address, amount])

evm_delegations_list.sort(key=lambda x: x[3],
