forest = {
    "id": "forest",
    "name": "🌳 The Forest",
    "description": "A dense forest filled with wild animals and mythical creatures. Many adventurers come to test their mettle against the beasts that dwell within.",
    "min_level_requirement": 1,
    "mini_boss_level_requirement": 5,
    "boss_level_requirement": 10,
    "enemies": {
        "regular": [
            {
                "id": "wild_boar",
                "loot_table": [
                    {"id": "boar_hide", "chance": 0.9, "quantity": [1, 3]},
                    {"id": "boar_tusk", "chance": 0.4, "quantity": [1, 2]},
                ],
            },
            {
                "id": "werewolf",
                "loot_table": [
                    {"id": "werewolf_pelt", "chance": 0.8, "quantity": [1, 3]},
                    {"id": "werewolf_fang", "chance": 0.3, "quantity": [1, 2]},
                ],
            },
            {
                "id": "harpy",
                "loot_table": [
                    {"id": "harpy_feather", "chance": 0.7, "quantity": [1, 3]},
                    {"id": "sharp_talon", "chance": 0.4, "quantity": [1, 2]},
                ],
            },
            {
                "id": "zombie",
                "loot_table": [
                    {"id": "rotten_flesh", "chance": 0.9, "quantity": [1, 5]},
                    {"id": "zombie_brain", "chance": 0.2, "quantity": [1, 1]},
                ],
            },
            {
                "id": "giant_python",
                "loot_table": [
                    {"id": "snake_skin", "chance": 0.8, "quantity": [1, 3]},
                    {"id": "venom_sac", "chance": 0.3, "quantity": [1, 2]},
                ],
            },
        ],
        "mini_boss": [
            {
                "id": "corrupted_fairy",
                "loot_table": [
                    {"id": "fairy_dust", "chance": 0.7, "quantity": [1, 2]},
                    {"id": "corrupted_crystal", "chance": 0.4, "quantity": [1, 2]},
                ],
            },
            {
                "id": "treant",
                "loot_table": [
                    {"id": "treant_bark", "chance": 0.8, "quantity": [1, 2]},
                    {"id": "treant_leaf", "chance": 0.6, "quantity": [1, 3]},
                ],
            },
        ],
        "boss": {
            "id": "forest_wyvern",
            "loot_table": [
                {"id": "wyvern_scale", "chance": 0.8, "quantity": [1, 2]},
                {"id": "wyvern_claw", "chance": 0.4, "quantity": [1, 2]},
                {"id": "wyvern_fire_gland", "chance": 0.2, "quantity": [1, 1]},
            ],
        },
    },
}
