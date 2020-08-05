from boardwatch.models.platform import Platform

class PlatformFamily():
  platform_families = []

  def assess_all_matches(listing):
    for family in PlatformFamily.platform_families:
      family.assess_matches(listing)

  def __init__(self, id, name, platforms=[]):
    self.id = id
    self.name = name
    self.platforms = platforms
    
    PlatformFamily.platform_families.append(self)

  def assess_matches(self, listing):
    for platform in self.platforms:
      platform.assess_matches(listing)
