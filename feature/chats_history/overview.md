now we should have the option to start a new chat or load preivous chat - we should probably generate custom filename for each chat and a title store it - we can store it in a json file for now - later we move to a proper litesql database.
we would have 
     - chat id. 1,2,3,4 etc
     - chat title - the first 30 characters of the user 1st message.
     - chat filename - we could generate a nice names from a library similar to passphrase like 'window-sequel-hawk' instead of a list of strings right? what is the chance we might hit the same thing twice. or should we keep it a bad looking messy string to make it almost impossible to hit the same result twice.
    
we would ask the user in the menu if he wants to open a new chat or continue the old one. if he wants to conitnue the old one we should load the previous chats and let him select preferred chat using the arrows. - we probably need 'rich' or other library to do that - to make claudecode like navigation in the cli.

we should probably add that as a separate feature - ui