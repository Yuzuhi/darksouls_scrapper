header = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"}

spells = {
    'Sorceries': 'https://darksouls.wiki.fextralife.com/Sorceries',
    'Pyromancies': 'https://darksouls.wiki.fextralife.com/Pyromancies',
    'Miracles': 'https://darksouls.wiki.fextralife.com/Miracles'
}

weapons = {
    'Daggers': 'https://darksouls.wiki.fextralife.com/Daggers',
    'Straight Swords': 'https://darksouls.wiki.fextralife.com/Straight+Swords',
    'Greatswords': 'https://darksouls.wiki.fextralife.com/Greatswords',
    'Ultra Greatswords': 'https://darksouls.wiki.fextralife.com/Ultra+Greatswords',
    'Curved Swords': 'https://darksouls.wiki.fextralife.com/Curved+Swords',
    'Katanas': 'https://darksouls.wiki.fextralife.com/Katanas',
    'Curved Greatswords': 'https://darksouls.wiki.fextralife.com/Curved+Greatswords',
    'Piercing Swords': 'https://darksouls.wiki.fextralife.com/Piercing+Swords',
    'Axes': 'https://darksouls.wiki.fextralife.com/Axes',
    'Great Axes': 'https://darksouls.wiki.fextralife.com/Great+Axes',
    'Hammers': 'https://darksouls.wiki.fextralife.com/Hammers',
    'Great Hammers': 'https://darksouls.wiki.fextralife.com/Great+Hammers',
    'Fist Weapons': 'https://darksouls.wiki.fextralife.com/Fist+Weapons',
    'Spears': 'https://darksouls.wiki.fextralife.com/Spears',
    'Halberds': 'https://darksouls.wiki.fextralife.com/Halberds',
    'Whips': 'https://darksouls.wiki.fextralife.com/Whips',
    'Bows': 'https://darksouls.wiki.fextralife.com/Bows',
    'Great Bows': 'https://darksouls.wiki.fextralife.com/Greatbows',
    'Crossbows': 'https://darksouls.wiki.fextralife.com/Crossbows',
    'Catalysts': 'https://darksouls.wiki.fextralife.com/Catalysts',
    'Flames': 'https://darksouls.wiki.fextralife.com/Flames',
    'Talismans': 'https://darksouls.wiki.fextralife.com/Talismans'
}

shields = {'Shields': 'https://darksouls.wiki.fextralife.com/Shields'}

armor = {
    'Helms': 'https://darksouls.wiki.fextralife.com/Helms',
    'Chest Armor': 'https://darksouls.wiki.fextralife.com/Chest+Armor',
    'Gauntlets': 'https://darksouls.wiki.fextralife.com/Gauntlets',
    'Leggings': 'https://darksouls.wiki.fextralife.com/Leg+Armor',
    'Unique Armor': 'https://darksouls.wiki.fextralife.com/Unique+Armor'
}

rings = {'Rings': 'https://darksouls.wiki.fextralife.com/Rings'}

items = {
    'Ammunition': 'https://darksouls.wiki.fextralife.com/Ammunition',
    'Consumables': 'https://darksouls.wiki.fextralife.com/Consumables',
    'Embers': 'https://darksouls.wiki.fextralife.com/Embers',
    'Key Bonfire Items': 'https://darksouls.wiki.fextralife.com/Key+Bonfire+Items',
    'Keys': 'https://darksouls.wiki.fextralife.com/Keys',
    'Multiplayer Items': 'https://darksouls.wiki.fextralife.com/Multiplayer+Items',
    'Ore': 'https://darksouls.wiki.fextralife.com/Ore',
    'Projectiles': 'https://darksouls.wiki.fextralife.com/Projectiles',
    'Souls': 'https://darksouls.wiki.fextralife.com/Souls',
    'Tools': 'https://darksouls.wiki.fextralife.com/Tools',
    'Unequippable': 'https://darksouls.wiki.fextralife.com/Unequippable'
}


dsr_page = 'https://darksouls.wiki.fextralife.com'

xpath_spells = "//tr/td[contains(@style,'center')]//a[@class='wiki_link']/@href"

xpath_weapons = "//tr/td[contains(@style,'center')]//a[@class='wiki_link']/@href"
xpath_armor = "//tr/td[contains(@style,'center')]//a[@class='wiki_link']/@href"
xpath_rings = "//tr/td[contains(@style,'center')]//a[@class='wiki_link']/@href"
xpath_items = "//tr/td[contains(@style,'center')]//a[@class='wiki_link']/@href"
xpath_shields = "//*[@id='wiki-content-block']/div/div/a/@href"

spells_equipment_name_xpath = '//*[@id="infobox"]/div/table/tbody/tr/*[@colspan="2"]//img/@src'
# default_equipment_name_xpath = "//*[@id=‘infobox’]/div/table/tbody/tr/*[@colspan='20']//img/@src" # weapons + shields + armor +
default_equipment_name_xpath = "//tbody/tr/*[@colspan='20']//img/@src"

# rings_items_equipment_name_xpath = "//*[@id='infobox']//@src"
rings_items_equipment_name_xpath ='//*[@id="infobox"]//h2//text()'
# items_equipment_name_xpath = "//*[@id='infobox']/div/table/thead/tr/th/h3/text()"

# 找到notes标签，找此标签的下面一组标签

# //*[contains(text(),'Notes')]/following-sibling::ul[1]

CATEGORY_LIST = ['Spells','Weapons', 'Shields',  'Armor', 'Rings',  'Items']