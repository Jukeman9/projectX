chat needs to be renamed from chat_history.json to unique name, coolname library later, maybe timestamp for now.
we need to store the data about all new chats in history_index.json - after the first user sent message to avoid storing empty chats ✅

current issues:
1. chat_id
- issue: is a static value
- solution: import cool-name library and generate a random 3 word string
- solution implemented: random strings for now (learning purposes) ✅



when starting the app we should introduce another option to resume a previous chat

1. user clicks option 2 resume previous chat
2. load history_index.json
3. display a numbered list off all the chat from the file
4. ask user for input 
5. load the specific chat
6. print the last 3 messages

current issues:
1. turn_id
- issue: we are resetting the turns each time the chat starts. If the chat has a history we should load the turn instead.
- solution: we should check from the chat_history.json if file has any history and append turn based on that. ✅

2. how to load chat from index?
- issue: we are loading chat directly from chat_history.json
- solution:
    1. first we need to save the chat to /chats/ with id as the name instead of chat_history.json ✅
    2. then when the user clicks resume chat we should load the list of the chat_titles and their timestamp in our terminal window
    3. maybe we should always start with option 1. start a new chat and then proceed to display chats below and change main menu from start a new chat and resume chat to just 1 option Chat and leave the menu for config stuff. 
    4. when the user clicks a particular chat we should load the history just like we do now but for that specific chat_id