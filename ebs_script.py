import boto3

class Volume:

    volume_costs = {"gp3": 0.08, "gp2": 0.10, "io1": 0.12, "st1": 0.045, "sc1": 0.015}

    def __init__(self, volume_type, volume_size, volume_id, creation_date):
        self.volume_type = volume_type
        self.volume_size = volume_size
        self.volume_id = volume_id
        self.creation_date = creation_date


    def get_volume_estimate(self):
        type_cost = self.volume_costs.get(self.volume_type)
        total_cost = type_cost * self.volume_size
        return total_cost

client = boto3.client('ec2')

response = client.describe_volumes(
    Filters=[
        {
            'Name': 'status',
            'Values': ['available']
        }
    ]
)


list_of_volumes = []

sorted_list_of_volumes = {}

for vol in response['Volumes']:
    ebs_volume = Volume(vol['VolumeType'], vol['Size'], vol['VolumeId'], vol['CreateTime'])
    list_of_volumes.append(ebs_volume)

print ("Volume ID                 Size         Type          Date_created                    Monthly cost")
for volume in list_of_volumes:

    name = volume.volume_id
    cost = Volume.get_volume_estimate(volume)
    sorted_list_of_volumes[name] = cost
    print(f"{volume.volume_id}      {volume.volume_size}           {volume.volume_type}        {volume.creation_date}"
          f"       {cost}     ")




