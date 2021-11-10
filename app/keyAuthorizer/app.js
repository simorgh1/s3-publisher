exports.handler = function (event, context, callback) {
  console.log("Received event:", JSON.stringify(event, null, 2));

  // Retrieve request parameters from the Lambda function input:
  var headers = event.headers;
  var queryStringParameters = event.queryStringParameters;

  // Perform authorization to return the Allow policy for correct parameters and
  // the 'Unauthorized' error, otherwise.

  if (
    headers.authorization === process.env.Authorizer_API_KEY &&
    queryStringParameters.target === "xray"
  ) {
    callback(null, generateAllow("me", event.routeArn));
  } else {
    callback("Unauthorized");
  }
};

// Help function to generate an IAM policy
var generatePolicy = function (principalId, effect, resource) {
  // Required output:
  var authResponse = {};
  authResponse.principalId = principalId;
  if (effect && resource) {
    var policyDocument = {};
    policyDocument.Version = "2012-10-17"; // default version
    policyDocument.Statement = [];
    var statementOne = {};
    statementOne.Action = "execute-api:Invoke"; // default action
    statementOne.Effect = effect;
    statementOne.Resource = resource;
    policyDocument.Statement[0] = statementOne;
    authResponse.policyDocument = policyDocument;
  }

  // Optional output with custom properties of the String, Number or Boolean type.

  var tmp = resource.split(":");
  var awsAccountId = tmp[4];
  var region = tmp[3];

  var tmp2 = tmp[5].toString().split("/");
  var apiId = tmp2[0];
  var stage = tmp2[1];
  var method = tmp2[2];
  var route = tmp2[3];

  authResponse.context = {
    name: "apikeyauthorizer",
    created: Date.now(),
    accountId: awsAccountId,
    region: region,
    apiId: apiId,
    stage: stage,
    method: method,
    route: route,
  };
  return authResponse;
};

var generateAllow = function (principalId, resource) {
  return generatePolicy(principalId, "Allow", resource);
};

var generateDeny = function (principalId, resource) {
  return generatePolicy(principalId, "Deny", resource);
};
