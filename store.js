import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/services/api'

Vue.use(Vuex)

// 認証情報
const authModule = {
    strict: process.env.NODE_ENV !== 'production',
    namespace: true,
    state: {
        username: '',
        isLoggerdIn: false
    },
    getters: {
        username: state => state.username,
        isLoggerdIn: state => state.isLoggerdIn
    },
    mutations: {
        set(state, payload) {
            state.username = payload.user.username
            state.isLoggerdIn = true
        },
        clear(state) {
            state.username = ''
            state.isLoggerdIn = false
        }
    },
    actions: {
        /**
         * ログイン
         */
        login(context, payload) {
            return api.post('/auth/jwt/create/', {
                'username': payload.username,
                'password': payload.password
            })
                .then(response => {
                    // 認証用トークンをlocalStorageに保存
                    localStorage.setItem('access', response.data.access)
                    // ユーザ情報を取得してstoreのユーザ情報を更新
                })
        },
        /**
         * ログアウト
         */
        logout(context) {
            // 認証用トークンをlocalStorageから削除
            localStorage.removeItem('access')
            // storeのユーザ情報をクリア
            context.commit('crear')
        },
        /**
         * ユーザ情報更新
         */
        reload(context) {
            return api.get('/auth/users/me/')
                .then(response => {
                    const user = response.data
                    // storeのユーザ情報を更新
                    context.commit('set', {user: user})
                    return user
                })
        }
    }
}
// グローバルメッセージ
const messageModule = {
    strict: process.env.NODE_ENV !== 'production',
    namespaced: true,
    state: {
        error: '',
        warnings: [],
        info: ''
    },
    getters: {
        error: state => state.error,
        warnings: state => state.warnings
    },
    mutations: {
        set(state, payload) {
            if (payload.error) {
                state.error = payload.error
            }
            if (payload.warnings) {
                state.warnings = payload.warnings
            }
            if (payload.info) {
                state.info = payload.info
            }
        },
        clear(state) {
            state.error = ''
            state.warnings = ''
            state.info
        }
    },
    actions: {
        /**
         * エラーメッセージ表示
         */
        setErrorMessage(context, payload) {
            context.commit('clear')
            context.commit('set', {'error': payload.message})
        },
        /**
         * 警告メッセージ（複数）表示
         */
        setWarningMessages(context, payload) {
            context.commit('clear')
            context.commit('set', {'warnings': payload.messages})
        },
        /**
         * インフォメーションメッセージ表示
         */
        setInfoMessage(context, payload) {
            context.commit('clear')
            context.commit('set', {'info': payload.message})
        },
        /**
         * 全メッセージ削除
         */
        clearMessages(context) {
            context.commit('clear')
        }
    }
}
const store = new Vuex.Store({
    modules: {
        auth: authModule,
        message: messageModule
    }
})

export default store