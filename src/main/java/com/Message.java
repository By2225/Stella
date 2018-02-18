package com;

// Spring utilizes the Jackson JSON library to automatically marshall instances
// of type Message into JSON
public class Message {

        private final String name;
        private final String amount;

        public Message(String name, String amount) {
            this.name = name;
            this.amount = amount;
        }

        public String getName() {
            return name;
        }

        public String getAmount() {
            return amount;
        }
    }

