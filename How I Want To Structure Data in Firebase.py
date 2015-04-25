"""

Right now, I'm just considering how to structure stations, first names, and
see-again choices.

...I guess I can't really have the station be at a parent level, since the
user at each station changes every subround. So maybe, for right now, I don't 
have to incorporate the station number at all. But we'll see.

"""

Option 1:

{
    "see-again-choices-R1": {

        "users": {
            
            "user1": {
                "no": 12,
                "maybe-no": 1,
                "maybe-yes": 10,
                "yes": 4
            },

            "user2": {
                "no": 2,
                "maybe-no": 5,
                "maybe-yes": 7,
                "yes": 13
            },    

            "user3": { 
                "no": 8, 
                "maybe-no": 6,
                "maybe-yes": 3,
                "yes": 1
            }                  
        },

        "choices": {

            "no": {
                "user1": 3,
                "user2": 7,
                "user3": 2
            },

            "maybe-no": {
                "user1": 0,
                "user2": 1,
                "user3": 5
            },

            "maybe-yes": {
                "user1": 12,
                "user2": 7,
                "user3": 4
            },

            "yes": {
                "user1": 9,
                "user2": 11,
                "user3": 14
            }

        }

    }






    //






    //

}


































"""