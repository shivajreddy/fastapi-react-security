import { removeAuthState, setAuthState } from "@/features/auth/authSlice"
import { useAppDispatch } from "@/hooks/hooks"
import { RootState } from "@/redux/store"
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"

const BASE_URL = "http://localhost:8000"
const REFRESH_TOKEN_ENDPOINT = "/refresh"

const baseQuery = fetchBaseQuery({
  baseUrl: BASE_URL,
  credentials: 'include',
  prepareHeaders: (headers, { getState }) => {
    const accessToken = (getState() as RootState).auth.accessToken;
    if (accessToken) {
      headers.set("authorization", `Bearer ${accessToken}`)
    }
    return headers;
  }
})


const baseQueryWithReAuth = async (args, api, extraOptions) => {
  let result = await baseQuery(args, api, extraOptions);
  console.log("result=", result);
  // const dispatch = useAppDispatch();

  if (result?.error?.status === 403) {
    const refreshResult = await baseQuery(REFRESH_TOKEN_ENDPOINT, api, extraOptions);
    console.log("refreshResult=", refreshResult);
    if (refreshResult?.data) {
      const user = api.getState().auth.user;
      // store the token
      // dispatch(setAuthState({ ...refreshResult.data, user }))
      api.dispatch(setAuthState({ ...refreshResult.data, user }))
      // retry original query with access token
      result = await baseQuery(args, api, extraOptions);
    }
  } else {
    // dispatch(removeAuthState());
    api.dispatch(removeAuthState());
  }
  return result;
}



export const apiSlice = createApi({
  baseQuery: baseQueryWithReAuth,
  endpoints: (builder) => ({})
})
