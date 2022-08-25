from django.urls import path
from satta_king import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
      path('', views.Login,name='login'),
      path('signup', views.SignUp,name='signup'),
      path('home', views.Home,name='home'),
      path('logout', views.logout,name='logout'),
      path('wallet', views.Wallet,name='wallet'),
      path('manage_bank', views.Bank,name='bank'),
      path('winning', views.Winning,name='winning'),
      path('bid', views. BID,name='bid'),
      path('gamesrate', views.GamesRate,name='gamesrate'),
      path('Conatct_us', views.Conatct,name='conatct'),
      path('ChangePassword', views.ChangePassword,name='ChangePassword'),
      path('howtoplay', views.HowToPlay,name='howtoplay'),
      path('add_point', views.ADDPOINT,name='addpoint'),
      path('starline', views.STARLINE,name='starline'),
      path('galidiswar', views.GALIDISWAR,name='galidiswar'),
      # MILAN MORNING
      path('milan_morning', views.MILANMORING,name='milan_morning'),
      path('singledigit', views.MILANMORNINGSINGLEDIGIT,name='milansingledigit'),
      path('jodidigit', views.MILANMORNINGJODIDIGIT,name='milanjodidigit'),
      path('milanmoringsinglepanna', views.MILANMORNINGSINGLEPANNA,name='milanmoringsinglepanna'),
      path('milanmoringdoublepanna', views.MILANMORNINGDOUBLEPANNA,name='milanmoringdoublepanna'),
      path('milanmoringtriplepanna', views.MILANMORNINGTRIPLEPANNA,name='milanmoringtriplepanna'),
      path('milanmoringhalfsangam', views.MILANMORNINGHALFSANGAM,name='milanmoringhalfsangam'),
      path('milanmoringfullsangam', views.MILANMORNINGFULLSANGAM,name='milanmoringfullsangam'),
      # WELCOME MORNING
      path('welcome_morning', views.WELCOMEMORNING,name='welcome_morning'),
      path('welcomemoringsingledigit', views.WELCOMEMORNINGSINGLEDIGIT,name='welcomemoringsingledigit'),
      path('welcomemoringjodidigit', views.WELCOMEMORNINGJODIDIGIT,name='welcomemoringjodidigit'),
      path('welcomemoringsinglepana', views.WELCOMEMORNINGSINGLEPANNA,name='welcomemorningsinglepana'),
      path('welcomemorningdoublepana', views.WELCOMEMORNINGDOUBLEPANNA,name='welcomemorningdoublepana'),
      path('welcomemorningtriplepanna', views.WELCOMEMORNINGTRIPLEPANNA,name='welcomemorningtriplepana'),
      path('welcomrmorninghalfsangam', views.WELCOMEMORNINGHALFSANGAM,name='welcomemorninghalfsangam'),
      path('welcomemorningfullsangam', views.WELCOMEMORNINGFULLSANGAM,name='welcomemorningfullsangam'),
      # KALYAN MORNING
      path('kalyan_morning', views.KALYANMORNING,name='kalyan_morning'),
      path('kalyanmorningsingledigit', views.KALYANMORINGSINGLEDIGIT,name='kalyanmoringsingledigit'),
      path('Kalyanmorningjodidigit', views.KALYANMORINGJODIDIGIT,name='kalyanmorningjodidigit'),
      path('Kalyanmornigsinglepana', views.KALYANMORINGSINGLEPANA,name='kalyanmorningsinglepana'),
      path('Kalyanmorningdoublepana', views.KALYANMORINGDOUBLEPANA,name='kalyanmorningdoublepana'),
      path('Kalyanmorningtriplepana', views.KALYANMORNINGTRIPLEPANA,name='kalyanmorningtriplepana'),
      path('Kalyanmorninghalfsangam', views.KALYANMORINGJHALFSANGAM,name='kalyanmorninghalfsangam'),
      path('Kalyanmorningfullsangam', views.KALYANMORINGFULLSANGAM,name='kalyanmorningfullsangam'),
      # MADHUR MORNING
      path('madhur_morning', views.MADHURMORNING,name='madhur_morning'),
      path('madhurmorningsingledigit', views.MADHURMORNINGSINGLEDIGIT,name='madhurmoringsingledigit'),
      path('madhurmorningjodidigit', views.MADHURMORINGJODIDIGIT,name='madhurmorningjodidigit'),
      path('madhurmorningsinglepana', views.MADHURMORINGSINGLEPANA,name='madhurmorningsinglepana'),
      path('madhurmorningdoublepana', views.MADHURMORINGDOUBLEPANA,name='madhurmorningdoublepana'),
      path('madhurmorningtriplepanna', views.MADHURMORINGTRIPLEPANA,name='madhurmorningtriplepanna'),
      path('madhurmorninghalfsangam', views.MADHURMORINGHALFSANGAM,name='madhurmorninghalfsangam'),
      path('madhurmorningfullsangam', views.MADHURMORINGFULLSANGAM,name='madhurmorningfullsangam'),
      #  SRIDEVI
      path('sridevi', views.SRIDEVI,name='sridevi'),
      path('sridevisingledigit', views.SRIDEVISINGLEDIGIT,name='sridevisingledigit'),
      path('sridevijodidigit', views.SRIDEVIJODIDIGIT,name='sridevijodidigit'),
      path('sridevisinglepana', views.SRIDEVISINGLEPANA,name='sridevisinglepana'),
      path('sridevidoublepana', views.SRIDEVIDOUBLEPANA,name='sridevidoublepana'),
      path('sridevitriplepanna', views.SRIDEVITRIPLEPANA,name='sridevitriplepanna'),
      path('sridevihalfsangam', views.SRIDEVIHALFSANGAM,name='sridevihalfsangam'),
      path('sridevifullsangam', views.SRIDEVIFULLSANGAM,name='sridevifullsangam'),
      # TIMEBAZAR
      path('timebazar', views.TIMEBAZAR,name='timebazar'),
      path('timebazarsingledigit', views.TIMEBAZARSINGLEDIGIT,name='timebazarsingledigit'),
      path('timebazarjodidigit', views.TIMEBAZARJODIDIGIT,name='timebazarjodidigit'),
      path('timebazarsinglepana', views.TIMEBAZARSINGLEPANA,name='timebazarsinglepana'),
      path('timebazardoublepanna', views.TIMEBAZARDOUBLEPANA,name='timebazardoublepanna'),
      path('timebazartriplepana', views.TIMEBAZARTRIPLEPANA,name='timebazartriplepana'),
      path('timebazarhalfsangam', views.TIMEBAZARHALFSANGAM,name='timebazarhalfsangam'),
      path('timebazarfullsangam', views.TIMEBAZARFULLSANGAM,name='timebazarfullsangam'),
      # MADHUR DAY
      path('madhurday', views.MADHURDAY,name='madhurday'),
      path('madhurdaysingledigit', views.MADHURDAYSINGLEDIGIT,name='madhurdaysingledigit'),
      path('madhurdayjodidigit', views.MADHURDAYJODIDIGIT,name='madhurdayjodidigit'),
      path('madhurdaysinglepana', views.MADHURDAYSINGLEPANA,name='madhurdaysinglepana'),
      path('madhurdaydoublepana', views.MADHURDAYDOUBLEPANA,name='madhurdaydoublepana'),
      path('madhurdaytriplepana', views.MADHURDAYTRIPLEPANA,name='madhurdaytriplepana'),
      path('madhurdayhalfsangam', views.MADHURDAYHALFSANGAM,name='madhurdayhalfsangam'),
      path('madhurdayfullsangam', views.MADHURDAYFULLSANGAM,name='madhurdayfullsangam'),
      # NEWKALYAN
      path('newkalyan', views.NEWKALYAN,name='newkalyan'),
      path('newkalyansingledigit', views.NEWKALYANSINGLEDIGIT,name='newkalyansingledigit'),
      path('newkalyanjodidigit', views.NEWKALYANJODIDIGIT,name='newkalyanjodidigit'),
      path('newkalyansinglepana', views.NEWKALYANSINGLEPANA,name='newkalyansinglepana'),
      path('newkalyandoublepana', views.NEWKALYANDOUBLEPANA,name='newkalyandoublepana'),
      path('newkalyantriplepana', views.NEWKALYANTRIPLEPANA,name='newkalyantriplepana'),
      path('newkalyanhalfsangam', views.NEWKALYANHALFSANGAM,name='newkalyanhalfsangam'),
      path('newkalyanfullsangam', views.NEWKALYANFULLSANGAM,name='newkalyanfullsangam'),
      # MILANDAY
      path('milanday', views.MILANDAY,name='milanday'),
      path('milandaysingledigit', views.MILANDAYSINGLEDIGIT,name='milandaysingledigit'),
      path('milandayjodidigit', views.MILANDAYJODIDIGIT,name='milandayjodidigit'),
      path('milandaysinglepana', views.MILANDAYSINGLEPANA,name='milandaysinglepana'),
      path('milandaydoublepana', views.MILANDAYDOUBLEPANA,name='milandaydoublepana'),
      path('milandaytriplepana', views.MILANDAYTRIPLEPANA,name='milandaytriplepana'),
      path('milandayhalfsangam', views.MILANDAYHALFSANGAM,name='milandayhalfsangam'),
      path('milandayfullsangam', views.MILANDAYFULLSANGAM,name='milandayfullsangam'),
      # RAJDANI DAY
      path('rajdhaniday', views.RAJDHANIDAY,name='rajdhaniday'),
      path('rajdhanisingledigit', views.RAJDHANIDAYSINGLEDIGIT,name='rajdhanisingledigit'),
      path('rajdhanijodidigit', views.RAJDHANIDAYJODIDIGIT,name='rajdhanijodidigit'),
      path('rajdhanidaysinglepana', views.RAJDHANIDAYJSINGLEPANA,name='rajdhanidaysinglepana'),
      path('rajdhanidaydoublepana', views.RAJDHANIDAYDOUBLEPANA,name='rajdhanidaydoublepana'),
      path('rajdhanidaytriplepana', views.RAJDHANIDAYTRIPLEPANA,name='rajdhanidaytriplepana'),
      path('rajdhanidayhalfsangam', views.RAJDHANIDAYHALFSANGAM,name='rajdhanidayhalfsangam'),
      path('rajdhanidayfullsangam', views.RAJDHANIDAYFULLSANGAM,name='rajdhanidayfullsangam'),
      # SUPREME DAY
      path('supremeday', views.SUPREMEDAY,name='supremeday'),
      path('supremedaysingledigit', views.SUPREMEDAYSINGLEDIGIT,name='supremedaysingledigit'),
      path('supremedayjodidigit', views.SUPREMEDAYJODIDIGIT,name='supremedayjodidigit'),
      path('supremedaysinglepana', views.SUPREMEDAYSINGLEPANA,name='supremedaysinglepana'),
      path('supremedaydoublepana', views.SUPREMEDAYDOUBLEPANA,name='supremedaydoublepana'),
      path('supremedaytriplepana', views.SUPREMEDAYTRIPLEPANA,name='supremedaytriplepana'),
      path('supremedayhalfsangam', views.SUPREMEDAYHALFSANGAM,name='supremedayhalfsangam'),
      path('supremedayfullsangam', views.SUPREMEDAYFULLSANGAM,name='supremedayfullsangam'),
      # KALYAN
      path('kalyan', views.KALYAN,name='kalyan'),
      path('kalyansingledigit', views.KALYANSINGLEDIGIT,name='kalyansingledigit'),
      path('kalyanjodidigit', views.KALYANJODIDIGIT,name='kalyanjodidigit'),
      path('kalyansinglepana', views.KALYANSINGLEPANA,name='kalyansinglepana'),
      path('kalyandoublepana', views.KALYANDOUBLEPANA,name='kalyandoublepana'),
      path('kalyantriplepana', views.KALYANTRIPLEPANA,name='kalyantriplepana'),
      path('kalyanhalfsangam', views.KALYANHALFSANGAM,name='kalyanhalfsangam'),
      path('kalyanfullsangam', views.KALYANFULLSANGAM,name='kalyanfullsangam'),
      # SRIDEVI NIGHT
      path('sridevinight', views.SRIDEVINIGHT,name='sridevinight'),
      path('sridevinightsingledigit', views.SRIDEVINIGHTSINGLEDIGIT,name='sridevinightsingledigit'),
      path('sridevinightjodidigit', views.SRIDEVINIGHTJODIDIGIT,name='sridevinightjodidigit'),
      path('sridevinightsinglepana', views.SRIDEVINIGHTSINGLEPAMNA,name='sridevinightsinglepana'),
      path('sridevinightdoublepana', views.SRIDEVINIGHTDOUBLEPANA,name='sridevinightdoublepana'),
      path('sridevinighttriplepana', views.SRIDEVINIGHTTRIPLEPANA,name='sridevinighttriplepana'),
      path('sridevinighthalfsangam', views.SRIDEVINIGHTHALFSANGAM,name='sridevinighthalfsangam'),
      path('sridevinightfullsangam', views.SRIDEVINIGHTFULLSANGAM,name='sridevinightfullsangam'),
      # MADHUR NIGHT 
      path('madhurnight', views.MADHURINIGHT,name='madhurnight'),
      path('madhurnightsingledigit', views.MADHURNIGHTSINGLEDIGIT,name='madhurnightsingledigit'),
      path('madhurnightjodidigit', views.MADHURNIGHTJODIDIGIT,name='madhurnightjodidigit'),
      path('madhurnightsinglepana', views.MADHURNIGHTSINGLEPANA,name='madhurnightsinglepana'),
      path('madhurnightdoublepana', views.MADHURNIGHTDOUBLEPANA,name='madhurnightdoublepana'),
      path('madhurnighttriplepana', views.MADHURNIGHTTRIPLEPANA,name='madhurnighttriplepana'),
      path('madhurnighthalfsangam', views.MADHURNIGHTHALFSANGAM,name='madhurnighthalfsangam'),
      path('madhurnightfullsangam', views.MADHURNIGHTFULLSANGAM,name='madhurnightfullsangam'),
      # NEW MAIN MUMBAI
      path('newmainmumbai', views.NEWMAINMUMBAI,name='newmainmumbai'),
      path('newmainmumbaisingledigit', views.NEWMAINMUMBAISINGLEDIGIT,name='newmainmumbaisingledigit'),
      path('newmainmumbaijodidigit', views.NEWMAINMUMBAIJODIDIGIT,name='newmainmumbaijodidigit'),
      path('newmainmumbaisinglepana', views.NEWMAINMUMBAISINGLEPANA,name='newmainmumbaisinglepana'),
      path('newmainmumbaidoublepana', views.NEWMAINMUMBAIDOUBLEPANA,name='newmainmumbaidoublepana'),
      path('newmainmumbaitriplepana', views.NEWMAINMUMBAITRIPLEPANA,name='newmainmumbaitriplepana'),
      path('newmainmumbaihalfsangam', views.NEWMAINMUMBAIHALFSANGAM,name='newmainmumbaihalfsangam'),
      path('newmainmumbaifullsangam', views.NEWMAINMUMBAIFULLSANGAM,name='newmainmumbaifullsangam'),
      # SUPREME NIGHT
      path('supremenight', views.SUPREMENIGHT,name='supremenight'),
      path('supremenightsingledigit', views.SUPREMENIGHTSINGLEDIGIT,name='supremenightsingledigit'),
      path('supremenightjodidigit', views.SUPREMENIGHTJODIDIGIT,name='supremenightjodidigit'),
      path('supremenightsinglepana', views.SUPREMENIGHTSINGLEPANA,name='supremenightsinglepana'),
      path('supremenightdoublepana', views.SUPREMENIGHTDOUBLEPANA,name='supremenightdoublepana'),
      path('supremenighttriplepana', views.SUPREMENIGHTTRIPLEPANA,name='supremenighttriplepana'),
      path('supremenighthalfsangam', views.SUPREMENIGHTHALFSANGAM,name='supremenighthalfsangam'),
      path('supremenightfullsangam', views.SUPREMENIGHTFULLSANGAM,name='supremenightfullsangam'),
      # MILAN NIGHT
      path('milannight', views.MILANNIGHT,name='milannight'),
      path('milannightsingledigit', views.MILANNIGHTSINGLEDIGIT,name='milannightsingledigit'),
      path('milannightjodidigit', views.MILANNIGHTJODIDIGIT,name='milannightjodidigit'),
      path('milannightsinglepana', views.MILANNIGHTSINGLEPANA,name='milannightsinglepana'),
      path('milannightdoublepana', views.MILANNIGHTDOUBLEPANA,name='milannightdoublepana'),
      path('milannighttriplepana', views.MILANNIGHTJTRIPLEPANA,name='milannighttriplepana'),
      path('milannighthalfsangam', views.MILANNIGHTHALFSANGAM,name='milannighthalfsangam'),
      path('milannightfullsangam', views.MILANNIGHTFULLSANGAM,name='milannightfullsangam'),
      # KALYAN NIGHT
      path('kalyannight', views.KALYANNIGHT,name='kalyannight'),
      path('kalyannightsingledigit', views.KALYANNIGHTSINGLEDIGIT,name='kalyannightsingledigit'),
      path('kalyannightjodidigit', views.KALYANNIGHTJODIDIGIT,name='kalyannightjodidigit'),
      path('kalyannightsinglepana', views.KALYANNIGHTSINGLEPANA,name='kalyannightsinglepana'),
      path('kalyannightdoublepana', views.KALYANNIGHTDOUBLEPANA,name='kalyannightdoublepana'),
      path('kalyannighttriplepana', views.KALYANNIGHTTRIPLEPANA,name='kalyannighttriplepana'),
      path('kalyannighthalfsangam', views.KALYANNIGHTHALFSANGAM,name='kalyannighthalfsangam'),
      path('kalyannightfullsangam', views.KALYANNIGHTFULLSANGAM,name='kalyannightfullsangam'),
      # RAJDHANI NIGHT
      path('rajdhaninight', views.RAJDHANINIGHT,name='rajdhaninight'),
      path('rajdhaninightsingledigit', views.RAJDHANINIGHTSINGLEDIGIT,name='rajdhaninightsingledigit'),
      path('rajdhaninightjodidigit', views.RAJDHANINIGHTJODIDIGIT,name='rajdhaninightjodidigit'),
      path('rajdhaninightsinglepana', views.RAJDHANINIGHTSINGLEPANA,name='rajdhaninightsinglepana'),
      path('rajdhaninightdoublepana', views.RAJDHANINIGHTDOUBLEPANA,name='rajdhaninightdoublepana'),
      path('rajdhaninighttriplepana', views.RAJDHANINIGHTTRIPLEPANA,name='rajdhaninighttriplepana'),
      path('rajdhaninighthalfsangam', views.RAJDHANINIGHTHALFSANGAM,name='rajdhaninighthalfsangam'),
      path('rajdhaninightfullsangam', views.RAJDHANINIGHTFULLSANGAM,name='rajdhaninightfullsangam'),
      # MAIN BAZAR
      path('mainbazar', views.MAINBAZAR,name='mainbazar'),
      path('mainbazarsingledigit', views.MAINBAZARSINGLEDIGIT,name='mainbazarsingledigit'),
      path('mainbazarjodidigit', views.MAINBAZARJODIDIGIT,name='mainbazarjodidigit'),
      path('mainbazarsinglepana', views.MAINBAZARSINGLEPANA,name='mainbazarsinglepana'),
      path('mainbazardoublepana', views.MAINBAZARDOUBLEPANA,name='mainbazardoublepana'),
      path('mainbazartriplepana', views.MAINBAZARTRIPLEPANA,name='mainbazartriplepana'),
      path('mainbazarhalfsangam', views.MAINBAZARHALFSANGAM,name='mainbazarhalfsangam'),
      path('mainbazarfullsangam', views.MAINBAZARFULLSANGAM,name='mainbazarfullsangam'),
      # STARLINE TIME
      path('10am', views.TENAM,name='10am'),
      path('11am', views.ELEVENAM,name='11am'),
      path('12pm', views.TWELEPM,name='12pm'),
      path('01pm', views.ONEPM,name='01pm'),
      path('02pm', views.TWOPM,name='02pm'),
      path('03pm', views.THREEPM,name='03pm'),
      path('04pm', views.FOURPM,name='04pm'),
      path('05pm', views.FIVEPM,name='05pm'),
      path('06pm', views.SIXPM,name='06pm'),
      path('07pm', views.SEVEANPM,name='07pm'),
      path('08pm', views.EIGHTPM,name='08pm'),
      path('09pm', views.NINEPM,name='09pm'),
      path('10pm', views.TENPM,name='10pm'),
      # 10AM
      path('tenamsingledigit', views.TENAMSINGLEDIGIT,name='tenamsingledigit'),
      path('tenamsinglepana', views.TENAMSINGLEPANA,name='tenamsinglepana'),
      path('tenamdoublepana', views.TENAMDOUBLEPANA,name='tenamdoublepana'),
      path('tenamtriplepana', views.TENAMTRIPLEPANA,name='tenamtriplepana'),
      # 11 AM
      path('elevensingledigit', views.ELEVENAMSINGLEDIGIT,name='elevensingledigit'),
      path('elevensinglepana', views.ELEVENAMSINGLEPANA,name='elevensinglepana'),
      path('elevendoublepana', views.ELEVENAMDOUBLEPANA,name='elevendoublepana'),
      path('eleventriplepana', views.ELEVENAMTRIPLEPANA,name='eleventriplepana'),
      # 12PM
      path('twelvepmsingledigit', views.TWELEPMSINGLEDIGIT,name='twelvepmsingledigit'),
      path('twelvepmsinglepana', views.TWELEPMSINGLEPANA,name='twelvepmsinglepana'),
      path('twelvepmdoublepana', views.TWELEPMDOUBLEPANA,name='twelvepmdoublepana'),
      path('twelvepmtriplepana', views.TWELEPMTRIPLEPANA,name='twelvepmtriplepana'),
      # 01PM
      path('onepmsingledigit', views.ONEPMSINGLEDIGIT,name='onepmsingledigit'),
      path('onepmsinglepana', views.ONEPMSINGLEPANA,name='onepmsinglepana'),
      path('onepmdoublepana', views.ONEPMDOUBLEPANA,name='onepmdoublepana'),
      path('onepmtriplepana', views.ONEPMTRIPLEPANA,name='onepmtriplepana'),
      # 02PM
      path('twopmsingledigit', views.TWOPMSINGLEDIGIT,name='twopmsingledigit'),
      path('twopmsinglepana', views.TWOPMSINGLEPANA,name='twopmsinglepana'),
      path('twopmdoublepana', views.TWOPMDOUBLEPANA,name='twopmdoublepana'),
      path('twopmtriplepana', views.TWOPMTRIPLEPANA,name='twopmtriplepana'),
      # 03PM
      path('threepmsingledigit', views.THREEPMSINGLEDIGIT,name='threepmsingledigit'),
      path('threepmsinglepana', views.THREEPMSINGLEPANA,name='threepmsinglepana'),
      path('threepmdoublepana', views.THREEPMDOUBLEPANA,name='threepmdoublepana'),
      path('threepmtriplepana', views.THREEPMTRIPLEPANA,name='threepmtriplepana'),
      # 04PM
      path('fourpmsingledigit', views.FOURPMSINGLEDIGIT,name='fourpmsingledigit'),
      path('fourpmsinglepana', views.FOURPMSINGLEPANA,name='fourpmsinglepana'),
      path('fourpmdoublepana', views.FOURPMDOUBLEPANA,name='fourpmdoublepana'),
      path('fourpmtriplepana', views.FOURPMTRIPLEPANA,name='fourpmtriplepana'),
      # 05PM
      path('fivepmsingledigit', views.FIVEPMSINGLEDIGIT,name='fivepmsingledigit'),
      path('fivepmsinglepana', views.FIVEPMSINGLEPANA,name='fivepmsinglepana'),
      path('fivepmdoublepana', views.FIVEPMDOUBLEPANA,name='fivepmdoublepana'),
      path('fivepmtriplepana', views.FIVEPMTRIPLEPANA,name='fivepmtriplepana'),
      # 06 PM
      path('sixpmsingledigit', views.SIXPMSINGLEDIGIT,name='sixpmsingledigit'),
      path('sixpmsinglepana', views.SIXPMSINGLEPANA,name='sixpmsinglepana'),
      path('sixpmdoublepana', views.SIXPMDOUBLEPANA,name='sixpmdoublepana'),
      path('sixpmtriplepana', views.SIXPMTRIPLEPANA,name='sixpmtriplepana'),
      # 07 PM
      path('sevenpmsingledigit', views.SEVENPMSINGLEDIGIT,name='sevenpmsingledigit'),
      path('sevenpmsinglepana', views.SEVENPMSINGLEPANA,name='sevenpmsinglepana'),
      path('sevenpmdoublepana', views.SEVENPMDOUBLEPANA,name='sevenpmdoublepana'),
      path('sevenpmtriplepana', views.SEVENPMTRIPLEPANA,name='sevenpmtriplepana'),
      
      # 08 PM
      path('eightpmsingledigit', views.EIGHTPMSINGLEDIGIT,name='eightpmsingledigit'),
      path('eightpmsinglepana', views.EIGHTPMSINGLEPANA,name='eightpmsinglepana'),
      path('eightpmdoublepana', views.EIGHTPMDOUBLEPANA,name='eightpmdoublepana'),
      path('eightpmtriplepana', views.EIGHTPMTRIPLEPANA,name='eightpmtriplepana'),
      
      # 09 PM
      path('ninepmsingledigit', views.NINEPMSINGLEDIGIT,name='ninepmsingledigit'),
      path('ninepmsinglepana', views.NINEPMSINGLEPANA,name='ninepmsinglepana'),
      path('ninepmdoublepana', views.NINEPMDOUBLEPANA,name='ninepmdoublepana'),
      path('ninepmtriplepana', views.NINEPMTRIPLEPANA,name='ninepmtriplepana'),
      # 10 PM
      path('tenpmsingledigit', views.TENPMSINGLEDIGIT,name='tenpmsingledigit'),
      path('tenpmsinglepana', views.TENPMSINGLEPANA,name='tenpmsinglepana'),
      path('tenpmdoublepana', views.TENPMDOUBLEPANA,name='tenpmdoublepana'),
      path('tenpmtriplepana', views.TENPMTRIPLEPANA,name='tenpmtriplepana'),
      # GALIDISAWAR
      path('disawar', views.DISAWAR,name='disawar'),
      path('faridabaad', views.FARIDABAAD,name='faridabaad'),
      path('gaziabaad', views.GAZIABAAD,name='gaziabaad'),
      path('gali', views.GALI,name='gali'),
      
  
      
    ]
if settings.DEBUG:
      urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)