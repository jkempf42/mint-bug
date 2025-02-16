## Mint bug

This repo illustrates two bugs in mint:

1) The originally reported bug in 
Mint removes Python modules if modules are loaded dynamically #752

2) Another discovered while creating the repo. It results in the following
error message when an HTTP request is sent to the container and the 
Python code in the container tries to return:

>
> info: Function.mint_bug_example[1]
>       Executing 'Functions.mint_bug_example' (Reason='This function was programmatically called via the host APIs.', Id=ec1e6faf-5377-4330-bd81-ebf586bd1003)
>info: Function.mint_bug_example.User[0]
      Python HTTP trigger function processed a request.
>fail: Function.mint_bug_example[3]
>      Executed 'Functions.mint_bug_example' (Failed, Id=ec1e6faf-5377-4330-bd81-ebf586bd1003, Duration=60ms)
>      Microsoft.Azure.WebJobs.Host.FunctionInvocationException: Exception while executing function: Functions.mint_bug_example
>       ---> System.IO.FileNotFoundException: Could not load file or assembly 'Microsoft.CSharp, Version=8.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a'. The system cannot find the file specified.
      
>       File name: 'Microsoft.CSharp, Version=8.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a'
>         at Microsoft.Azure.WebJobs.Script.Grpc.GrpcMessageExtensionUtilities.ConvertFromHttpMessageToExpando(RpcHttp inputMessage)
>         at Microsoft.Azure.WebJobs.Script.Grpc.GrpcMessageConversionExtensions.ToObject(TypedData typedData) in /src/azure-functions-host/src/WebJobs.Script.Grpc/MessageExtensions/GrpcMessageConversionExtensions.cs:line 35
>         at Microsoft.Azure.WebJobs.Script.Grpc.GrpcWorkerChannel.CreateScriptInvocationResult(InvocationResponse invokeResponse) in /src/azure-functions-host/src/WebJobs.Script.Grpc/Channel/GrpcWorkerChannel.cs:line 1154
>         at Microsoft.Azure.WebJobs.Script.Grpc.GrpcWorkerChannel.InvokeResponse(InvocationResponse invokeResponse) in /src/azure-functions-host/src/WebJobs.Script.Grpc/Channel/GrpcWorkerChannel.cs:line 1123
>         at Microsoft.Azure.WebJobs.Script.Description.WorkerFunctionInvoker.InvokeCore(Object[] parameters, FunctionInvocationContext context) in /src/azure-functions-host/src/WebJobs.Script/Description/Workers/WorkerFunctionInvoker.cs:line 101

>    (more after this)

## Code

The code is a simple Azure Functions function app that takes an HTTP request
`/api/mint_bug_example` with query parameter `name` and if the name is not
`Darth_Vader` returns a hello message. If it is `Darth_Vader`, it
uses the Python module `importlib` to dynamically load the module `darth_vader` and call the function `enter_darth_vader()`.

## Build container, start container, test for Python import bug

The bash script `build-mint-bug.sh` builds the container `mint-bug`.

After the container is build, start it with `start-container.sh`, then
run `test-mint-python-import-bug.sh` to illustrate how it should work.

Then run mint on it like this:

`mint build --http-probe --expose 80 mint-bug:latst`

Then run the mint container using `start-bug-container.sh` and run
`test-mint-python-import-bug.sh` again.

The failure to find the dynamically loaded module message will show up.

## Test for C# file missing bug

Mint seems to be also removing code necessary for the Azure Functions runtime
to return. That's the second bug mentioned above. The user code here is
Python, there's no C# but the error message says that Microsoft.CSharp is 
missing. 

The build and start procedure is as before, but this time run 
`test-mint-azure-functions-csharp-bug.sh`against the running container.
