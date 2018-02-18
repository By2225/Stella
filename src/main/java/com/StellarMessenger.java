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

@RestController
public class StellarMessenger {
    @RequestMapping("/")
    public String welcome(){
        return "You have successfully connected to the Stellar Facebook Messenger API!";
    }

    @RequestMapping("/createKeyPair")
    public static KeyPair createKeyPair(){
        // Generates seed for creating a key pair
        KeyPair pair = KeyPair.random();
        System.out.println(pair.getSecretSeed());
        System.out.println(pair.getAccountId());
        return pair;
    }

    @RequestMapping("/registerTestNetAccount")
    public static String registerTestNetAccount(@RequestParam(value="accountId") String accountId) throws Exception{
        // Registers account with the TestNet
        String friendBotUrl = String.format(
                "https://horizon-testnet.stellar.org/friendbot?addr=%s",
                accountId);
        InputStream response = new URL(friendBotUrl).openStream();
        String responseBody = new Scanner(response, "UTF-8").useDelimiter("\\A").next();
        System.out.println("SUCCESS! You have a new account :)\n" + responseBody);
        return responseBody;
    }

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

    @RequestMapping("/send")
    public static SubmitTransactionResponse sendLumens(@RequestParam(value="secretSeed") String secretSeed,
                                  @RequestParam(value="destAcctId") String destAcctId,
                                  @RequestParam(value="amount") String amount) throws Exception {

        Server server = new Server("https://horizon-testnet.stellar.org");
        KeyPair source = KeyPair.fromSecretSeed(secretSeed);
        KeyPair destination = KeyPair.fromAccountId(destAcctId);
        Network.useTestNetwork();
        // Checks if destination account exists
        // If account does not exist HttpResponseException will be thrown
        server.accounts().account(destination);
        // Load up to date information about
        AccountsRequestBuilder sourceAccountBuilder = server.accounts();

        // Throws HttpResponseException if error
        AccountResponse sourceAccount = sourceAccountBuilder.account(source);

        // Build the transaction
        Transaction.Builder transactionBuilder = new Transaction.Builder(sourceAccount);
        // AssetTypeNative represents the Stellar Lumens Native asset
        PaymentOperation payment = new PaymentOperation.Builder(
                destination, new AssetTypeNative(), amount).build();

        // Add metadata to transaction (optional)
        transactionBuilder.addMemo(Memo.text("Test transaction"));
        Transaction transaction = transactionBuilder.addOperation(payment).build();

        transaction.sign(source); // sign transaction with private seed

        SubmitTransactionResponse response = null;
        // And finally, send it off to Stellar!
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
                // TODO: Check for actual response from Horizon server. Resubmit if no reponse
            }
        }
        return response;
    }
}
