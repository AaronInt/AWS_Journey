# This script will create an EC2 instance that installs apache and is deployed onto a cloud environment.

## Steps:

<ol>
  <li>Create VPC</li>
  <li>Create Internet Gateway</li>
  <li>Create Custom Route Table</li>
  <li>Create a Subnet</li>
  <li>Associate subnet with Route Table</li>
  <li>Create Security Group to allow port 22,88, 443</li>
  <li> Create a network interface with an ip in the subnet that was created in step 4</li>
  <li>Assign an elastic IP to the network interface created in step 7</li>
  <li>Create Ubuntu server and install/enable apache2</li>
</ol>
