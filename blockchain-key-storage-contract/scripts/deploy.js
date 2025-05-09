async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);
  
  const DataKeyStorage = await ethers.getContractFactory("DataKeyStorage");
  const dataKeyStorage = await DataKeyStorage.deploy();
  
  await dataKeyStorage.waitForDeployment();

  console.log("DataKeyStorage deployed to:", await dataKeyStorage.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
