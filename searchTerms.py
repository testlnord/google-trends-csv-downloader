'''
    Here are all the terms we are going to download the trend data for.
    The ammount of data collected in files will be:
         total = geo_terms x periods_of_time x list_of_search_terms
    Approx: 3600 queries

'''


list_of_geo_terms = [
    "AU-ACT",
    "AU-NSW",
    "AU-NT",
    "AU-QLD",
    "AU-SA",
    "AU-TAS",
    "AU-VIC",
    "AU-WA",
    "AU",
]

list_of_categories = [
    "0-5-31",
]

'''
    Periods of time consist of a start date and a number of month
'''
list_of_periods_of_time = [
    '', #From Jan 2004 - present
    # '1/2009 67m', #From Jan 2009 lasting 67 months (July 2014)
]

list_of_search_terms = [
    '.net',
    'ActionScript',
    'ajax',
    'android',
    'Intent (Android)',
    'AngularJS',
    'Apache',
    'asp.net',
    'asp.net mvc',
    'azure cloud',
    'Backbone.js',
    'c',
    'c#',
    'C++',
    'CakePHP',
    'cocoa apple',
    'CodeIgniter',
    'PhoneGap',
    'css',
    'delphi',
    'django',
    'eclipse',
    'Entity Framework',
    'ExtJS',
    'Firefox',
    'Adobe Flash',
    'Apache Flex',
    'gcc',
    'git',
    'app engine',
    'Google Chrome',
    'Google Maps',
    'grails ',
    'gwt',
    'haskell',
    'Hibernate (Java)',
    'HTML',
    'HTML5',
    'http',
    'iis',
    'Internet Explorer',
    'IOS',
    'IPad',
    'IPhone',
    'java',
    '%2Fm%2F0bs6x',
    'JavaScript',
    'Java Persistence API',
    'JQuery',
    'JQuery Mobile',
    'JQuery UI',
    'jsf',
    'JSON',
    'jsp',
    'linq',
    'Linux',
    'Magento',
    'MATLAB',
    'Maven',
    'MongoDB',
    'Microsoft Access',
    'MySQL',
    'NHibernate',
    'Node.js',
    'Objective-C',
    'OpenCV',
    'OpenGL',
    'OS X',
    'Perl',
    'PHP',
    'PostgreSQL',
    'PowerShell',
    'Python language',
    'qt',
    'r',
    'ruby',
    'Ruby on Rails',
    'scala',
    'SharePoint',
    'silverlight',
    'Spring Framework',
    'SQL',
    'sql server',
    'SQLite',
    'svn',
    'Swing (Java)',
    'Symfony',
    'Apache Tomcat',
    'Transact-SQL',
    'twitter bootstrap',
    'Ubuntu',
    'Unix',
    'vb .net',
    'vba',
    'Visual C++',
    'Visual Studio',
    'wcf',
    'winapi',
    'windows',
    'wp7',
    'Windows Forms',
    'WordPress',
    'wpf',
    'xaml',
    'Xcode',
    'XSLT',
    'Zend Framework'
]


