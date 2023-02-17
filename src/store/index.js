/*vuex最核心的管理对象*/
import {createStore} from 'vuex'
import state from './state'
import mutations from './mutations'
import actions from './actions'
import getters from './getters'
export default createStore({
    state,
    mutations,
    actions,
    getters
})