import pytest
import pandas
from src.trader.indicator import EMACrossoverIndicator

@pytest.fixture()
def sample_data():
    price_dec_1_2_2017_json = '{"close":{"[1512838800]":230559200,"[1512839700]":226001000,"[1512840600]":221101100,"[1512841500]":212787900,"[1512842400]":233100100,"[1512843300]":228350100,"[1512844200]":230769000,"[1512845100]":229999700,"[1512846000]":229998900,"[1512846900]":228150000,"[1512847800]":229788000,"[1512848700]":229500000,"[1512849600]":230700100,"[1512850500]":230898800,"[1512851400]":234000500,"[1512852300]":234999900,"[1512853200]":234000900,"[1512854100]":236899800,"[1512855000]":235799600,"[1512855900]":238198200,"[1512856800]":237500000,"[1512857700]":239450300,"[1512858600]":240000000,"[1512859500]":242600500,"[1512860400]":244999500,"[1512861300]":242800400,"[1512862200]":243000000,"[1512863100]":238210400,"[1512864000]":237000000,"[1512864900]":233991300,"[1512865800]":230899500,"[1512866700]":234000000,"[1512867600]":230279000,"[1512868500]":226700300,"[1512869400]":221312200,"[1512870300]":220399900,"[1512871200]":228500400,"[1512872100]":223299300,"[1512873000]":222589000,"[1512873900]":220500400,"[1512874800]":218000000,"[1512875700]":217700000,"[1512876600]":211000000,"[1512877500]":202101100,"[1512878400]":206499000,"[1512879300]":205000000,"[1512880200]":202000000,"[1512881100]":206000000,"[1512882000]":205000300,"[1512882900]":203848900,"[1512883800]":202999500,"[1512884700]":203440000,"[1512885600]":207699900,"[1512886500]":209208100,"[1512887400]":213005000,"[1512888300]":214200000,"[1512889200]":214100900,"[1512890100]":214399600,"[1512891000]":215950000,"[1512891900]":215990300,"[1512892800]":216075000,"[1512893700]":211600000,"[1512894600]":214784500,"[1512895500]":214001100,"[1512896400]":213500000,"[1512897300]":213399800,"[1512898200]":215991000,"[1512899100]":215199900,"[1512900000]":218500000,"[1512900900]":219995300,"[1512901800]":225500000,"[1512902700]":223440100,"[1512903600]":226514100,"[1512904500]":226776900,"[1512905400]":223700500,"[1512906300]":225950400,"[1512907200]":224999500,"[1512908100]":223899400,"[1512909000]":224999900,"[1512909900]":225400700,"[1512910800]":229999000,"[1512911700]":233650000,"[1512912600]":234000000,"[1512913500]":239400000,"[1512914400]":251500100,"[1512915300]":246996400,"[1512916200]":242000000,"[1512917100]":236020400,"[1512918000]":231000000,"[1512918900]":242000000,"[1512919800]":243266300,"[1512920700]":241500000,"[1512921600]":239510200,"[1512922500]":243001000,"[1512923400]":240800100,"[1512924300]":239000000,"[1512925200]":235000100,"[1512926100]":236000200,"[1512927000]":238100800,"[1512927900]":239999800,"[1512928800]":238999500,"[1512929700]":238699200,"[1512930600]":238459400,"[1512931500]":238310400,"[1512932400]":240646500,"[1512933300]":240200000,"[1512934200]":242201000,"[1512935100]":245200300,"[1512936000]":241980000},"high":{"[1512838800]":232800000,"[1512839700]":230800000,"[1512840600]":226100000,"[1512841500]":222000100,"[1512842400]":235000000,"[1512843300]":238000000,"[1512844200]":232000000,"[1512845100]":234899000,"[1512846000]":232000000,"[1512846900]":229999000,"[1512847800]":229888100,"[1512848700]":229790000,"[1512849600]":230700100,"[1512850500]":231000100,"[1512851400]":235000000,"[1512852300]":239888900,"[1512853200]":236998900,"[1512854100]":239000500,"[1512855000]":238999000,"[1512855900]":239900000,"[1512856800]":239500900,"[1512857700]":239499800,"[1512858600]":240000000,"[1512859500]":242899900,"[1512860400]":245000000,"[1512861300]":244999900,"[1512862200]":243899900,"[1512863100]":243100600,"[1512864000]":240000000,"[1512864900]":237998800,"[1512865800]":233991300,"[1512866700]":234997800,"[1512867600]":234000100,"[1512868500]":230800600,"[1512869400]":226800000,"[1512870300]":222000000,"[1512871200]":229999700,"[1512872100]":229899100,"[1512873000]":227500200,"[1512873900]":222777700,"[1512874800]":222000000,"[1512875700]":218001000,"[1512876600]":217899700,"[1512877500]":212785400,"[1512878400]":216000000,"[1512879300]":214000600,"[1512880200]":207050200,"[1512881100]":206000000,"[1512882000]":214500100,"[1512882900]":205000300,"[1512883800]":203899400,"[1512884700]":203500000,"[1512885600]":209090000,"[1512886500]":210000000,"[1512887400]":214500600,"[1512888300]":224918900,"[1512889200]":217999100,"[1512890100]":214800000,"[1512891000]":217200000,"[1512891900]":215990300,"[1512892800]":217000000,"[1512893700]":216849900,"[1512894600]":216000000,"[1512895500]":214915000,"[1512896400]":215000700,"[1512897300]":214013200,"[1512898200]":215991000,"[1512899100]":217502700,"[1512900000]":219784100,"[1512900900]":221000000,"[1512901800]":230000000,"[1512902700]":227799000,"[1512903600]":227000000,"[1512904500]":226799900,"[1512905400]":226999900,"[1512906300]":226000000,"[1512907200]":225999000,"[1512908100]":224999500,"[1512909000]":225800900,"[1512909900]":225688700,"[1512910800]":229999000,"[1512911700]":233700000,"[1512912600]":239100900,"[1512913500]":239400000,"[1512914400]":251500100,"[1512915300]":261899000,"[1512916200]":246996400,"[1512917100]":242000100,"[1512918000]":236500200,"[1512918900]":243837000,"[1512919800]":247097400,"[1512920700]":243266300,"[1512921600]":241799000,"[1512922500]":243001000,"[1512923400]":243814500,"[1512924300]":240800100,"[1512925200]":239000000,"[1512926100]":238100100,"[1512927000]":238500500,"[1512927900]":240499300,"[1512928800]":239999900,"[1512929700]":238999500,"[1512930600]":238699200,"[1512931500]":238459400,"[1512932400]":241000000,"[1512933300]":240899900,"[1512934200]":242500000,"[1512935100]":246898900,"[1512936000]":245200400},"low":{"[1512838800]":230500700,"[1512839700]":225623800,"[1512840600]":218000000,"[1512841500]":206599900,"[1512842400]":212000000,"[1512843300]":223305100,"[1512844200]":226000900,"[1512845100]":228000400,"[1512846000]":228010200,"[1512846900]":228000300,"[1512847800]":228000000,"[1512848700]":228500000,"[1512849600]":228500000,"[1512850500]":230000100,"[1512851400]":230252500,"[1512852300]":234000000,"[1512853200]":232599700,"[1512854100]":233000000,"[1512855000]":233499500,"[1512855900]":234100100,"[1512856800]":237012400,"[1512857700]":237100000,"[1512858600]":239000700,"[1512859500]":239999900,"[1512860400]":242501400,"[1512861300]":242350400,"[1512862200]":242800400,"[1512863100]":238098500,"[1512864000]":237000000,"[1512864900]":232000100,"[1512865800]":230500000,"[1512866700]":230001000,"[1512867600]":230100000,"[1512868500]":225000000,"[1512869400]":220999700,"[1512870300]":220000500,"[1512871200]":220300500,"[1512872100]":222500600,"[1512873000]":222581600,"[1512873900]":220500000,"[1512874800]":215786000,"[1512875700]":216750000,"[1512876600]":210000000,"[1512877500]":202000000,"[1512878400]":201500000,"[1512879300]":205000000,"[1512880200]":200000000,"[1512881100]":201778100,"[1512882000]":203010000,"[1512882900]":203023500,"[1512883800]":202829900,"[1512884700]":202500000,"[1512885600]":203440000,"[1512886500]":204000000,"[1512887400]":207000500,"[1512888300]":209800000,"[1512889200]":213000000,"[1512890100]":213000000,"[1512891000]":214000000,"[1512891900]":214000300,"[1512892800]":214000000,"[1512893700]":210503200,"[1512894600]":209000200,"[1512895500]":212180000,"[1512896400]":213100100,"[1512897300]":213012100,"[1512898200]":212180100,"[1512899100]":213700000,"[1512900000]":214001000,"[1512900900]":215499000,"[1512901800]":219900100,"[1512902700]":222000000,"[1512903600]":223400100,"[1512904500]":224600000,"[1512905400]":223600600,"[1512906300]":222459900,"[1512907200]":224100200,"[1512908100]":223101500,"[1512909000]":223305000,"[1512909900]":224080000,"[1512910800]":225000000,"[1512911700]":227510000,"[1512912600]":233650000,"[1512913500]":233000000,"[1512914400]":238900100,"[1512915300]":243304800,"[1512916200]":238495000,"[1512917100]":236016500,"[1512918000]":228218900,"[1512918900]":228519200,"[1512919800]":240555500,"[1512920700]":239000000,"[1512921600]":239500000,"[1512922500]":239510100,"[1512923400]":240000200,"[1512924300]":239000000,"[1512925200]":235000100,"[1512926100]":235000100,"[1512927000]":235201100,"[1512927900]":238100800,"[1512928800]":238999500,"[1512929700]":238500000,"[1512930600]":238000000,"[1512931500]":237000000,"[1512932400]":237990000,"[1512933300]":240000000,"[1512934200]":240200000,"[1512935100]":242000200,"[1512936000]":241000000},"open":{"[1512838800]":231000800,"[1512839700]":230559200,"[1512840600]":226001000,"[1512841500]":221101100,"[1512842400]":212787900,"[1512843300]":233100100,"[1512844200]":228350100,"[1512845100]":230769000,"[1512846000]":229999700,"[1512846900]":229998900,"[1512847800]":228150000,"[1512848700]":229788000,"[1512849600]":229500000,"[1512850500]":230700100,"[1512851400]":230898800,"[1512852300]":234000500,"[1512853200]":234999900,"[1512854100]":234000900,"[1512855000]":236899800,"[1512855900]":235799600,"[1512856800]":238198200,"[1512857700]":237500000,"[1512858600]":239450300,"[1512859500]":240000000,"[1512860400]":242600500,"[1512861300]":244999500,"[1512862200]":242800400,"[1512863100]":243000000,"[1512864000]":238210400,"[1512864900]":237000000,"[1512865800]":233991300,"[1512866700]":230899500,"[1512867600]":234000000,"[1512868500]":230279000,"[1512869400]":226700300,"[1512870300]":221312200,"[1512871200]":220399900,"[1512872100]":228500400,"[1512873000]":223299300,"[1512873900]":222589000,"[1512874800]":220500400,"[1512875700]":218000000,"[1512876600]":217700000,"[1512877500]":211000000,"[1512878400]":202101100,"[1512879300]":206499000,"[1512880200]":205000000,"[1512881100]":202000000,"[1512882000]":206000000,"[1512882900]":205000300,"[1512883800]":203848900,"[1512884700]":202999500,"[1512885600]":203440000,"[1512886500]":207699900,"[1512887400]":209208100,"[1512888300]":213005000,"[1512889200]":214200000,"[1512890100]":214100900,"[1512891000]":214399600,"[1512891900]":215950000,"[1512892800]":215990300,"[1512893700]":216075000,"[1512894600]":211600000,"[1512895500]":214784500,"[1512896400]":214001100,"[1512897300]":213500000,"[1512898200]":213399800,"[1512899100]":215991000,"[1512900000]":215199900,"[1512900900]":218500000,"[1512901800]":219995300,"[1512902700]":225500000,"[1512903600]":223440100,"[1512904500]":226514100,"[1512905400]":226776900,"[1512906300]":223700500,"[1512907200]":225950400,"[1512908100]":224999500,"[1512909000]":223899400,"[1512909900]":224999900,"[1512910800]":225400700,"[1512911700]":229999000,"[1512912600]":233650000,"[1512913500]":234000000,"[1512914400]":239400000,"[1512915300]":251500100,"[1512916200]":246996400,"[1512917100]":242000000,"[1512918000]":236020400,"[1512918900]":231000000,"[1512919800]":242000000,"[1512920700]":243266300,"[1512921600]":241500000,"[1512922500]":239510200,"[1512923400]":243001000,"[1512924300]":240800100,"[1512925200]":239000000,"[1512926100]":235000100,"[1512927000]":236000200,"[1512927900]":238100800,"[1512928800]":239999800,"[1512929700]":238999500,"[1512930600]":238699200,"[1512931500]":238459400,"[1512932400]":238310400,"[1512933300]":240646500,"[1512934200]":240200000,"[1512935100]":242201000,"[1512936000]":245200300},"volume":{"[1512838800]":9.10297135,"[1512839700]":31.46136036,"[1512840600]":65.69105922,"[1512841500]":78.685341,"[1512842400]":73.71749514,"[1512843300]":45.63268454,"[1512844200]":17.20577405,"[1512845100]":18.35796399,"[1512846000]":9.33337084,"[1512846900]":5.47593411,"[1512847800]":9.29681952,"[1512848700]":3.43149032,"[1512849600]":5.66034608,"[1512850500]":2.57339353,"[1512851400]":9.07226567,"[1512852300]":8.50887346,"[1512853200]":4.88276651,"[1512854100]":4.33670289,"[1512855000]":3.89141615,"[1512855900]":5.56535642,"[1512856800]":3.46052576,"[1512857700]":7.63506097,"[1512858600]":5.20211256,"[1512859500]":14.34620602,"[1512860400]":11.93075165,"[1512861300]":5.73397654,"[1512862200]":5.23600219,"[1512863100]":12.67344809,"[1512864000]":5.25179893,"[1512864900]":15.25539404,"[1512865800]":10.7469722,"[1512866700]":10.4874953,"[1512867600]":6.75837062,"[1512868500]":31.61656539,"[1512869400]":17.4741671,"[1512870300]":21.81727886,"[1512871200]":25.59452362,"[1512872100]":13.08545877,"[1512873000]":22.19207707,"[1512873900]":21.38706193,"[1512874800]":25.84438006,"[1512875700]":32.28176885,"[1512876600]":48.26690938,"[1512877500]":61.87834959,"[1512878400]":58.39490333,"[1512879300]":27.23140051,"[1512880200]":85.90528532,"[1512881100]":40.36018093,"[1512882000]":34.30668154,"[1512882900]":18.03785218,"[1512883800]":26.75704946,"[1512884700]":11.52594915,"[1512885600]":21.27500537,"[1512886500]":15.51296821,"[1512887400]":26.32197868,"[1512888300]":60.13098161,"[1512889200]":17.79465219,"[1512890100]":12.47358813,"[1512891000]":12.4192136,"[1512891900]":6.64433534,"[1512892800]":15.6332024,"[1512893700]":17.96363319,"[1512894600]":21.58219924,"[1512895500]":5.67587725,"[1512896400]":5.25259057,"[1512897300]":5.44193059,"[1512898200]":8.18098525,"[1512899100]":13.18610203,"[1512900000]":11.09898429,"[1512900900]":26.55321942,"[1512901800]":27.84572161,"[1512902700]":20.98282422,"[1512903600]":13.13569096,"[1512904500]":6.74403429,"[1512905400]":9.40814058,"[1512906300]":17.66655189,"[1512907200]":8.78550911,"[1512908100]":3.72899554,"[1512909000]":15.22130118,"[1512909900]":3.97265761,"[1512910800]":15.19620484,"[1512911700]":40.78960587,"[1512912600]":54.70804228,"[1512913500]":30.21781391,"[1512914400]":84.25353185,"[1512915300]":118.29035709,"[1512916200]":63.90824048,"[1512917100]":23.76232249,"[1512918000]":35.8438581,"[1512918900]":44.6967142,"[1512919800]":45.82573321,"[1512920700]":29.25397694,"[1512921600]":7.82344515,"[1512922500]":8.91559677,"[1512923400]":9.50409494,"[1512924300]":8.42693267,"[1512925200]":11.85045688,"[1512926100]":5.7166888,"[1512927000]":5.84680996,"[1512927900]":3.31414413,"[1512928800]":3.4635082,"[1512929700]":2.19401691,"[1512930600]":1.55654545,"[1512931500]":0.53795886,"[1512932400]":3.0872042,"[1512933300]":1.9108873,"[1512934200]":6.2491108,"[1512935100]":20.00253503,"[1512936000]":9.39260877}}'
    price = pandas.read_json(price_dec_1_2_2017_json)
    price.index = [idx.replace('[', '').replace(']', '') for idx in price.index]
    return price

def test_constructor_accept_correct_data_size(sample_data):
    test_short = [20, 25, 30, 35]
    test_long = [45, 50, 60, 75]
    test_hold = [0, 10, 20, 30]
    for short_p, long_p, hold in zip(test_short, test_long, test_hold):
        size = long_p + hold
        indicator = EMACrossoverIndicator(sample_data.tail(size), short_p, long_p, confirm_period=hold)
        assert indicator.size == size

def test_constructor_reject_incorrect_data_size(sample_data):
    test_short = [20, 25, 30, 35]
    test_long = [45, 50, 60, 75]
    test_hold = [0, 10, 20, 30]
    wrong_size = [20, 50, 90, 40]
    for short_p, long_p, hold, size in zip(test_short, test_long, test_hold, wrong_size):
        with pytest.raises(RuntimeError) as excinfo:
            EMACrossoverIndicator(sample_data.tail(size), short_p, long_p, confirm_period=hold)
        assert 'Inconsistent data size with configuration' in str(excinfo)
        assert str(size) in str(excinfo)

def test_detect_sell_signal(sample_data):
    indicator = EMACrossoverIndicator(sample_data.head(70), 35, 50, confirm_period=20)
    assert indicator.is_sell_signal()

def test_detect_buy_signal(sample_data):
    indicator = EMACrossoverIndicator(sample_data.tail(70), 35, 50, confirm_period=20)
    assert indicator.is_buy_signal()

def test_not_getting_false_buy_signal(sample_data):
    indicator = EMACrossoverIndicator(sample_data.head(85).tail(70), 35, 50, confirm_period=20)
    assert not indicator.is_buy_signal()