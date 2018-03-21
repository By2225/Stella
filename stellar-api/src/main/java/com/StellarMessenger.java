package com;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.stellar.sdk.*;
import org.stellar.sdk.requests.AccountsRequestBuilder;
import org.stellar.sdk.responses.AccountResponse;
import org.stellar.sdk.responses.SubmitTransactionResponse;
import org.json.*;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.Scanner;

// TODO: Encrypt secret seed and remove print statements for sensitive sender_info
@RestController
public class StellarMessenger {

    /*
     @return Api welcome message
    */
    @RequestMapping("/")
    public String welcome(){
        return "You have successfully connected to the Stellar Facebook Messenger API!";
    }

    /*
       @return New account id and secret seed key pair
    */
    @RequestMapping("/createKeyPair")
    public static KeyPair createKeyPair(){
        // Generates seed for creating a key pair
        KeyPair pair = KeyPair.random();
        return pair;
    }

    /*
       Registers new test net account
       @param accountID Unregistered account id
       @return Account registration response
    */
    @RequestMapping("/registerTestNetAccount")
    public static String registerTestNetAccount(@RequestParam(value="accountId") String accountId) throws Exception{
        // Registers account with the TestNet
        String friendBotUrl = String.format(
                "https://horizon-testnet.stellar.org/friendbot?addr=%s",
                accountId);
        InputStream response = new URL(friendBotUrl).openStream();
        String responseBody = new Scanner(response, "UTF-8").useDelimiter("\\A").next();
        return responseBody;
    }

    /*
       Retrieves balance for Stellar account
       @param secretSeed Secret seed for Stellar account
       @return Account balance response
    */
    @RequestMapping("/getBalance")
    public static String getBalance(@RequestParam(value="accountId") String accountId) throws IOException {
        Server server = new Server("https://horizon-testnet.stellar.org");
        KeyPair pair = KeyPair.fromAccountId(accountId);
        AccountResponse account = server.accounts().account(pair); // throws IOException
        AccountResponse.Balance balance = account.getBalances()[0];
        String response = "Account: %s Stellar Balance: %s".format(pair.getAccountId(),
                balance.getBalance());
        JSONObject resp = new JSONObject();
        resp.put("account", pair.getAccountId());
        resp.put("balance", balance.getBalance());
        System.out.println(response);
        return resp.toString();
    }


    /*
      Sends Stellar lumens to destination account id
      @param secretSeed secret seed for sender account
      @param destAcctId destination account id
      @param amount amount to send
      @return Response for transaction submission request
    */
    @RequestMapping("/send")
    public static SubmitTransactionResponse sendLumens(@RequestParam(value="secretSeed") String secretSeed,
                                  @RequestParam(value="destAcctId") String destAcctId,
                                  @RequestParam(value="amount") String amount) throws Exception {
        Server server = new Server("https://horizon-testnet.stellar.org");
        KeyPair source = KeyPair.fromSecretSeed(secretSeed);
        KeyPair destination = KeyPair.fromAccountId(destAcctId);
        Network.useTestNetwork();

        // Checks if destination account exists, throws HttpResponseException for
        // nonexistent account
        server.accounts().account(destination);

        AccountsRequestBuilder sourceAccountBuilder = server.accounts();

        // Throws HttpResponseException source account does not exist
        AccountResponse sourceAccount = sourceAccountBuilder.account(source);

        Transaction.Builder transactionBuilder = new Transaction.Builder(sourceAccount);

        // AssetTypeNative is the Stellar Lumens Native asset
        PaymentOperation payment = new PaymentOperation.Builder(
                destination, new AssetTypeNative(), amount).build();

        Transaction transaction = transactionBuilder.addOperation(payment).build();
        transaction.sign(source); // sign transaction with private seed

        SubmitTransactionResponse response = null;

        // Submit transaction to Stellar
        int count = 0;
        while (count < 5) {
            try {
                count++;
                response = server.submitTransaction(transaction);
                System.out.println("Success!");
                System.out.println(response);
                break;
            } catch (Exception e) {
                System.out.println("Something went wrong! Retrying...");
                System.out.println(e.getMessage());
                // TODO: Check for actual response from Horizon server.
                // Resubmit if no reponse
            }
        }
        return response;
    }
}
