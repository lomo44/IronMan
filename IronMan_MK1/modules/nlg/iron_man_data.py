Iron_Man_NLG_DATA = {
    "ID" : "Iron_Man",
    "lex" : {
        "adverb" : {
            "absolutely" : {
                "verbal_strength" : 2.0
            },
            "really" : {
                "verbal_strength" : 1.5
            }
        },
        "prefix" : {
            "Well,": {
                "seriousness" : 0.9
            },
            "Tell you what,":{
                "seriousness" : 0.9
            } 
        },
        "preference" : {
            "like" : {
                "preference" : 0.5
            },
            "hate" : {
                "preference" : -0.5
            }
        },
        "be" : {
            "be" :{

            }
        },
        "greeting" : {
            "Hey!" :{
                "verbal_strength" : 1.0
            },
            "Hello!" : {
                "verbal_strength" : 1.0
            }
        }
    },
    "templates" : {
        "definition" : {
            "pattern" : "{prefix} [subject] {be} {adverb} [object]" 
        },
        "assertion" : {
            "pattern" : "{prefix} {assert} {adverb} {bool_assert}"
        },
        "preference" : {
            "pattern" : "{prefix} [subject] {adverb} {preference} [object]"
        },
        "greeting" : {
            "pattern" : "{greeting}"
        }
    },
    "default" : "Fuck Off"
}