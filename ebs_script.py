import boto3
from datetime import datetime, timezone

class Volume:

    volume_costs = {"gp3": 0.08, "gp2": 0.10, "io1": 0.12, "st1": 0.045, "sc1": 0.015}

    def __init__(self, volume_type, volume_size, volume_id, creation_date):
        self.volume_type = volume_type
        self.volume_size = volume_size
        self.volume_id = volume_id
        self.creation_date = creation_date


    def get_volume_estimate(self):
        type_cost = self.volume_costs.get(self.volume_type)
        if type_cost is None:
            print(f"Warning: Unknown volume type {self.volume_type}, using $0.10/GB default")
            type_cost = 0.10
        total_cost = type_cost * self.volume_size
        return total_cost

client = boto3.client('ec2')

try:
    response = client.describe_volumes(
        Filters=[
            {
            'Name': 'status',
            'Values': ['available']
            }
     ]
    )
except Exception as e:
    print(f"Error connecting to AWS: {e}")
    exit(1)

list_of_volumes = []

sorted_list_of_volumes = []

for vol in response['Volumes']:
    ebs_volume = Volume(vol['VolumeType'], vol['Size'], vol['VolumeId'], vol['CreateTime'])
    list_of_volumes.append(ebs_volume)


print("UNATTACHED EBS VOLUMES REPORT")
print("=" * 45)
print ("Volume ID               Size        Type       Days Old       Monthly cost")

total_monthly = 0
sorted_list = sorted(list_of_volumes, key=lambda v: v.get_volume_estimate(), reverse=True)


for volume in sorted_list:

    name = volume.volume_id
    cost = volume.get_volume_estimate()
    total_monthly += cost
    age_days = (datetime.now(timezone.utc) - volume.creation_date).days

    print(f"{volume.volume_id:<15} {volume.volume_size:>6} {volume.volume_type:>10}  {age_days:>10} {cost:>15}     ")

print("=" * 90)


print(f"Total Monthly Savings Potential: ${total_monthly}")
print(f"Annual Savings Potential: ${total_monthly * 12}")
