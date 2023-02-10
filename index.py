import os
import csv

print("Querying validators list...")
command = os.popen('cantod q staking validators')
full_validators = command.read()

only_val = full_validators.split("validators:")[1].split("\n- commission:")[1:]

val_addresses = []
for full_val in only_val:
val_adr = [adr for adr in full_val.split("\n") if "operator_address" in adr][0].strip().split("operator_address: ")[1]
val_addresses.append(val_adr)

print("Finding all delegations...")
user_delegations = {}
for adr in val_addresses:
command = os.popen('cantod q staking delegations-to ' + adr)
delegations = command.read()
only_del = delegations.split("delegation_responses:")[1].split("\n- balance:")[1:]

rew = 0
for dele in only_del:
    del_adr = [adr for adr in dele.split("\n") if "delegator_address" in adr][0].strip().split("delegator_address: ")[1]
    amount = int([adr for adr in dele.split("\n") if "amount" in adr][0].strip().split("amount: ")[1].replace('"', ""))

    user_delegations.append([adr, del_adr, amount])
print("Writing to staking.csv...")
with open("staking.csv", "w", newline="") as f:
writer = csv.writer(f)
writer.writerow(["Validator", "Delegator", "Amount"])
writer.writerows(user_delegations)

print("Done!")
