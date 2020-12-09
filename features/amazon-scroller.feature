Feature: Amazon challenge
  
  @fixture.browser_<browser>
  Scenario Outline: Amazon scroller <browser>
    Given we are browsing amazon
    When we search for "iPhone X"
    When we filter price "0" to "1000"
    When we filter "iOS"
    When we sort by price "High to Low"
    Then we log results

  Examples: browser
   | browser       | 
   | chrome        |
   | firefox       |
