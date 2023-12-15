import axios from 'axios';

// 증권 URL 주소
const STOCK_URL = "http://121.179.83.68:8881/stock_api";

// 차트 URL 주소
const CHART_API_BASE_URL = 'http://221.156.60.18:8081';

// 세션 객체 생성
const sessionStorage = window.sessionStorage

// const Alarm_url = "http://221.156.60.18:9101/alarm";

const STOCK_CODES = {
    // 코스피 리스트
    kospi: ['005930', '373220', '000660', '207940', '005935',
        '005490', '005380', '051910', '035420', '000270',
        '006400', '068270', '003670', '035720', '105560',
        '028260', '012330', '055550', '066570', '096770',
        '032830', '003550', '323410', '033780', '086790',
        '000810', '034730', '015760', '138040', '017670',
        '018260', '011200', '329180', '010130', '009150',
        '047050', '259960', '316140', '034020', '024110'],

    // 코스닥 리스트
    kosdaq: ['247540', '086520', '091990', '022100', '066970',
        '028300', '196170', '068760', '035900', '277810',
        '403870', '058470', '263750', '214150', '293490',
        '357780', '041510', '039030', '145020', '005290',
        '095340', '112040', '240810', '036930', '253450',
        '035760', '000250', '086900', '121600', '214370',
        '067310', '393890', '025900', '034230', '237690',
        '078600', '048410', '141080', '365340', '195940']
}

// 특정 주식의 차트 데이터를 가져오는 함수
function getSpecificChartData(state, type, stock) {
    // 주어진 타입의 차트 데이터 중에서 주식의 고유번호에 해당하는 데이터를 반환
    return state[type][stock.initial.stck_shrn_iscd];
}

// updateChartData Mutation이 시장 타입을 판별하기 위한 객체
const chartTypes = {
    'kospi': {
        'daily': 'dailyKospi',
        'week': 'weekKospi',
        'month': 'monthKospi'
    },
    'kosdaq': {
        'daily': 'dailyKosdaq',
        'week': 'weekKosdaq',
        'month': 'monthKosdaq'
    }
};
const intervalMap = {
    day: 'daily_stock',
    week: 'week_stock',
    month: 'month_stock'
};
//스토어 상태 정의
const state = {
    Stocks: [], // API로 가져온 80개 종목
    allStocks: [], // 모든 종목 주식
    myStocks: [], // 관심 주식
    Sentiments: {}, // 종목의 여론 데이터
    sessionMyStock: [], // 세션에서 가져온 사용자의 관심주식
    currentMarket: 'kospi', // 현재 사용자가 선택한 주식 시장 (기본값: 'kospi')
    dailyKospi: {_id: '', stock_data: []}, // 코스피 일봉차트
    weekKospi: {_id: '', stock_data: []}, // 코스피 주봉차트
    monthKospi: {_id: '', stock_data: []},// 코스피 월봉차트
    dailyKosdaq: {_id: '', stock_data: []}, // 코스닥 일봉차트
    weekKosdaq: {_id: '', stock_data: []}, // 코스닥 주봉차트
    monthKosdaq: {_id: '', stock_data: []},  // 코스닥 월봉차트
};

// 스토어 변이(Mutation) 정의
const mutations = {
    // API로 가져온 80개 종목 업데이트
    updateStock(state, stocks) {
        state.Stocks = stocks
    },
    // 모든 주식 목록을 업데이트
    updateAllStocks(state, stocks) {
        state.allStocks = stocks;
    },
    // 세션에서 가져온 관심종목 업데이트
    updatesessionMyStock(state, favoriteStocks) {
        state.sessionMyStock = favoriteStocks;
    },
    // 세션에서 관심종목 관심종목으로 변환
    updataMyStock(state, list) {
        state.myStocks = list
    },
    //일봉, 주봉, 월봉 차트 업데이트
    updateChartData(state, {type, data}) {
        const [market, interval] = type.split('_');
        const chartDataKey = chartTypes[market][interval];
        if (chartDataKey) {
            state[chartDataKey] = data;
        }
    },
    // 여론 업테이트
    updateSentiments(state, sentiments) {
        state.Sentiments = sentiments;
    },
    // 관심주식 추가
    addToMyStocks(state, stock) {
        state.myStocks.push(stock);
        state.allStocks = state.allStocks.filter(s => s.id !== stock.id);
    },
    // 관심주식제거
    removeFromMyStocks(state, stock) {
        state.myStocks = state.myStocks.filter(s => s.id !== stock.id);
        if (stock.market === state.currentMarket) {
            state.allStocks.push(stock);
        }
    },
    // 현재 사용자가 선택한 주식 시장 업데이트
    updateCurrentMarket(state, market) {
        state.currentMarket = market;
    },
    // 알림 설정을 추가
    addAlertSetting(state, alertSetting) {
        alertSetting.alerted = false; // 알림 발생 여부를 나타내는 속성 추가
        state.alertSettings.push(alertSetting);
    },

    // 알림 설정을 제거
    removeAlertSetting(state, stockId) {
        state.alertSettings = state.alertSettings.filter(setting => setting.stockId !== stockId);
    },

    // 모든 알림 설정의 alerted 속성을 false로 초기화
    resetAlerted(state) {
        state.alertSettings.forEach((setting) => {
            setting.alerted = false;
        });
    },
    // updateAlarm(state, {stck_shrn_iscd, response}) {(알람기능 테스트용)
    //     // 해당 종목에 대한 알림 정보 업데이트 또는 추가
    //     const index = state.stockalarm.findIndex(item => item.stck_shrn_iscd === stck_shrn_iscd);
    //
    //     if (index !== -1) {
    //         // 이미 있는 경우 업데이트
    //         state.stockalarm[index].response = response;
    //     } else {
    //         // 없는 경우 추가
    //         state.stockalarm.push({stck_shrn_iscd, response});
    //     }
    // },

    // 스토어 상태를 초기화
    resetState(state) {
        state.Stocks = []; // API로 가져온 80개 종목 초기화
        state.allStocks = [];  // 모든 종목 주식 초기화
        state.myStocks = [];  // 관심 주식 초기화
        state.dailyKospi = {_id: '', stock_data: []};  // 코스피 일봉 차트 초기화
        state.weekKospi = {_id: '', stock_data: []};  // 코스피 주봉 차트 초기화
        state.monthKospi = {_id: '', stock_data: []};  // 코스피 월봉 차트 초기화
        state.dailyKosdaq = {_id: '', stock_data: []};  // 코스닥 일봉 차트 초기화
        state.weekKosdaq = {_id: '', stock_data: []};  // 코스닥 주봉 차트 초기화
        state.monthKosdaq = {_id: '', stock_data: []};  // 코스닥 월봉 차트 초기화
        state.alertSettings = [] // 알람 기능초기화
        state.Sentiments = {}; // 여론 데이터 초기화
        state.cachedSentiments = {} // 여론 데이터를 캐싱하는 객체

    },

    // // SET_NOTIFICATION: 사용자가 알림을 설정할 때 호출되는 뮤테이션. 주식의 고유번호와 퍼센트를 인자로 받아 stockAlarm 상태를 변경
    // SET_NOTIFICATION(state, {stockId, percentage}) {
    //     const index = state.stockAlarm.findIndex(n => n.stockId === stockId);
    //     if (index !== -1) {
    //         // 이미 설정된 알림이 있으면, 퍼센트를 업데이트
    //         state.stockAlarm[index].percentage = percentage;
    //     } else {
    //         // 설정된 알림이 없으면, 새로운 알림을 추가
    //         state.stockAlarm.push({stockId, percentage});
    //     }
    // },
    // SET_PRICE_CHANGES: API로부터 받은 주식 가격 정보를 스토어에 저장하는 뮤테이션. 주식 가격 정보를 인자로 받아 priceChanges 상태를 변경
    // SET_PRICE_CHANGES(state, priceChanges) {
    //     state.priceChanges = priceChanges;
    // }
};

// 스토어 액션(Action) 정의
const actions = {
    // 모든 주식 정보를 가져오는 액션
    async fetchAllStocks({commit, state, dispatch}) {
        try {
            // 요청할 데이터
            const dataToBeSent = {
                "company": "0",
                "initial": ["stck_shrn_iscd", "COMPANY", "stck_prpr", "hts_avls", "acml_vol", "per",
                    "pbr", "eps", "stck_prdy_oprc", "stck_prdy_hgpr", "stck_prdy_lwpr", "acml_vol","prdy_vrss", "prdy_ctrt","stck_prdy_clpr","acml_vol","acml_tr_pbmn"
                ],
                "current_trade": ["STCK_PRPR", "ACML_VOL","PRDY_VRSS", "PRDY_CTRT","ACML_VOL","ACML_TR_PBMN"]
            };
            const response = await axios.post(`${STOCK_URL}`, dataToBeSent);
            if (!response.data) {
                console.log('API 응답에 데이터가 없습니다.');
                return;
            }
            const stocks = Object.values(response.data);
            // console.log("모든주식정보 API응답", stocks)

            commit("updateStock", stocks)
            console.log("여기는 오지??")
            // console.log("API를 통해 불러온 모든주식정보", stocks)
            const processedStocks = stocks.map(stock => {
                const id = stock.initial.stck_shrn_iscd;
                // 코스피 코스닥 판단
                const marketType = STOCK_CODES.kospi.includes(stock.initial.stck_shrn_iscd) ? 'kospi' : 'kosdaq';
                // current_trade를 사용하는데 안에 데이터가 없으면 initial사용
                const data = stock.current_trade && stock.current_trade.length > 0
                    ? stock.current_trade
                    : stock.initial && stock.initial.length > 0
                        ? stock.initial
                        : [];

                return {id, ...stock, data, market: marketType};

            });
            const sortedStocks = processedStocks.sort((a, b) => {
                return a.initial.COMPANY.localeCompare(b.initial.COMPANY);
            });


            // 현재 선택된 시장에 해당하는 주식만 필터링
            let filteredStocks = processedStocks.filter(stock => STOCK_CODES[state.currentMarket].includes(stock.initial.stck_shrn_iscd));
            // 관심 주식 목록에 있는 주식은 제외
            filteredStocks = filteredStocks.filter(stock => !state.myStocks.some(myStocks => myStocks.initial.stck_shrn_iscd === stock.initial.stck_shrn_iscd));
            commit('updateAllStocks', filteredStocks, sortedStocks);
            // console.log("관심 주식 목록에 있는 주식은 제외",filteredStocks)

            // updataMyStock을 최신화 시켜줌(id, market)
            const updatedMyStocks = state.myStocks.map((stock) =>
                processedStocks.find((s) => s.id === stock.id) || stock
            );



            // if (state.currentMarket === 'kospi') {
            //     state.sessionStock.forEach((stock) => {
            //         delete state.dailyKospi[stock.id];
            //     });
            // } else {
            //     state.sessionStock.forEach((stock) => {
            //         delete state.dailyKosdaq[stock.id];
            //     });
            // }
        } catch (error) {
            console.error('stockapi 에러:', error);
            setTimeout(() => {
                dispatch(' fetchAllStocks');
            }, 1000);
        }
    },

    // // 특정 주식을 관심 주식 목록에 추가하는 액션
    addToMyStocks({commit}, stock) {
        commit('addToMyStocks', stock);
    },

    // 특정 주식을 관심 주식 목록에서 제거하는 액션
    removeFromMyStocks({commit}, stock) {
        commit('removeFromMyStocks', stock);
    },

    updateMarket({commit, dispatch, state}, market) {
        commit('updateCurrentMarket', market);
        dispatch('fetchAllStocks').then(() => {
            const filteredStocks = state.allStocks.filter(stock => stock.market === state.currentMarket);
            commit('updateAllStocks', filteredStocks);
        });
    },
    // 알림 설정을 저장하는 액션
    async saveAlertSetting({commit}, alertSetting) {
        // 백엔드 API를 호출하여 알림 설정을 서버에 저장
        const response = await axios.get("http://221.156.60.18:9101/alarm", alertSetting);

        // API 호출이 성공하면
        if (response.status === 200) {
            // 'addAlertSetting' 뮤테이션을 커밋하여 Vuex 스토어의 상태를 업데이트
            commit('addAlertSetting', alertSetting);
        } else {
            // API 호출이 실패하면 오류 메시지를 콘솔에 출력
            console.error('API실패');
        }
    },

    // 알람기능 텟트
    // async alarmstock({commit}, {stockid, morLes, username, price}) {
    //     const url = "http://221.156.60.18:9101/alarm";
    //     try {
    //         const response = await axios.get(url);
    //         if (!response.data || !response.data.length) {
    //             return null;
    //         }
    //         console.log("알림기능 axios 데이터확인", response.data);
    //         commit('updatealarm', {stockid, response: response.data});
    //         console.log("updatealarm뮤테이션실행후 state.stocklarm값", state.stockalarm)
    //         const stockData = response.data.find(item => item.stock_num === stockid);
    //         console.log("stockData확인", stockData.percent_change)
    //         const isplus = function (stockData, price) {
    //             return stockData >= price;
    //         };
    //
    //         const isminus = function (stockDatae, price) {
    //             return stockData <= price;
    //         };
    //
    //         if (stockData) {
    //             if (morLes === "+") {
    //                 if (isplus(stockData.percent_change, price)) {
    //                     window.alert(`${username}님이 선택한 ${stockData.stock_num}이 ${stockData.percent_change}${price} 이상입니다.`);
    //                 }
    //             } else {
    //                 if (isminus(stockData.percent_change, price)) {
    //                     window.alert(`${username}님이 선택한 ${stockData.stock_num}이 ${stockData.percent_change}${price} 이하입니다.`);
    //                 }
    //             }
    //         } else {
    //             window.alert("해당하는 코드 없습니다.");
    //         }
    //     } catch (error) {
    //         console.error("Error occurred:", error);
    //         return null;
    //     }
    // },


    // 여론 데이터를 가져오는 액션
    async fetchAllSentiments({ commit }) {
        try {
            // 오늘 날짜를 변환하여 API에 요청
            const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
            console.log("today",today)
            const response = await axios.get(`http://221.156.60.18:8092/sentiment/count?date=${today}`);

            // API 응답에서 여론 데이터 추출
            const sentiments = response.data.stock_sentiment_count;

            // 여론 데이터를 state에 저장
            commit('updateSentiments', sentiments);
            console.log("여론API를 가져옴",sentiments)
        } catch (error) {
            console.error('여론 데이터를 가져오는 데 실패했습니다:', error);
        }
    },
    // 주식의 차트 데이터 가져오는 액션
    async fetchStockChartData({commit, state}, {stck_shrn_iscd, interval}) {
        const stock = state.Stocks.find(stock => stock.initial.stck_shrn_iscd === stck_shrn_iscd);
            console.log("차트액션 실행",stock)
        if (stock) {
            try {
                const _id = stock.initial.stck_shrn_iscd;

                let marketType = "";
                if (STOCK_CODES.kospi.includes(_id)) {
                    marketType = 'kospi';
                } else if (STOCK_CODES.kosdaq.includes(_id)) {
                    marketType = 'kosdaq';
                } else {
                    throw new Error(`알 수 없는 주식 코드: ${_id}`);
                }


                if (marketType) {
                    // console.log("marketType", marketType)
                    const mappedInterval = intervalMap[interval];

                    const response = await axios.post(`${CHART_API_BASE_URL}/${marketType}_${mappedInterval}/${_id}`);
                    // processChartData 함수의 내용을 직접 작성
                    console.log("주식차트 데이터 가져오는 액션", response)
                    const data = {
                        _id: response.data._id,
                        stock_data: response.data.stock_data
                    };
                    commit('updateChartData', {type: `${marketType}_${mappedInterval}`, data});
                    // console.log("fetchStockChartData실행 후 updateChartData뮤테이션으로 이동", data)

                }
            } catch (error) {
                console.error(`차트 데이터를 가져오는데 실패했습니다: ${error}`);
            }
        }
    },
    // 세션에서 사용자의 관심종목을 가져옴
    fetchFavoriteMyStocks({commit, state}) {
        const favoriteStocks = JSON.parse(sessionStorage.getItem(`favorite_stock`));
        if (favoriteStocks) {
            const list = [];
            commit('updatesessionMyStock', favoriteStocks);
            for (let i = 0; i < state.sessionMyStock.favorite_stock.length; i++) {
                for (let j = 0; j < state.Stocks.length; j++) {
                    if (state.Stocks[j].initial.stck_shrn_iscd == Object.keys(state.sessionMyStock.favorite_stock[i])[0]) {
                        list.push(state.Stocks[j]);
                    }
                }
            }
            commit('updataMyStock', list);
            const processedStocks = state.myStocks.map(stock => {
                const id = stock.initial.stck_shrn_iscd;
                // 코스피 코스닥 판단
                const marketType = STOCK_CODES.kospi.includes(stock.initial.stck_shrn_iscd) ? 'kospi' : 'kosdaq';
                return {id, ...stock, market: marketType};
            });
            // console.log("mystock확인",state.myStocks)
            commit('updataMyStock', processedStocks);
            console.log("사용자관심종목확인",state.myStocks)
        } else {
            console.log("사용자의 관심종목을 가져오는데 실패하였습니다.")
        }
    },

    // 모든 상태를 초기화
    resetStore({commit}) {
        commit('resetState');
    },
};

// 스토어 게터(Getter) 정의
const getters = {
    dailyKospi: state => state.dailyKospi,
    weekKospi: state => state.weekKospi,
    monthKospi: state => state.monthKospi,
    dailyKosdaq: state => state.dailyKosdaq,
    weekKosdaq: state => state.weekKosdaq,
    monthKosdaq: state => state.monthKosdaq,

    filteredAllStocks(state) {
        return state.allStocks.filter(stock => !state.myStocks.some(myStock => myStock.initial.stck_shrn_iscd === stock.initial.stck_shrn_iscd));
    },
    // // 현재 선택된 시장의 주식 목록을 필터링하여 반환하는 게터
    // getCurrentMarketStocks: (state) => {
    //     const filteredStocks = state.allStocks.filter(stock => STOCK_CODES[state.currentMarket].includes(stock.initial.stck_shrn_iscd));
    //     return filteredStocks;
    // },
    // 관심 주식 목록을 반환
    getMyStocks: (state) => state.myStocks,
    // 여론 데이터를 반환하는 게터
    getsentiment: (state) => (stockCode) => {
        // 캐시된 데이터가 있는지 확인하고 반환
        if (state.cachedSentiments[stockCode]) {
            return state.cachedSentiments[stockCode];
        }
        // 캐시된 데이터가 없을 경우 원격 서버에서 가져와 반환
        return state.sentiment.find((data) => data.stockCode === stockCode) || [];
    },
    // 주어진 종류(type)와 주식 코드(stockCode)에 해당하는 차트 데이터를 반환하는 게터
    getChartData: (state) => (type, stock) => getSpecificChartData(state, type, stock),
    // 현재 선택된 시장 정보를 반환(KOSPI, KOSDAQ)
    getCurrentMarket: (state) => state.currentMarket,

};

// Vuex 모듈로 만들어 내보냄
const StockPage = {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
};

export default StockPage;
