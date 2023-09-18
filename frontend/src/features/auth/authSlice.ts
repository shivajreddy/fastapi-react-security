import { PayloadAction, createSlice } from "@reduxjs/toolkit";
import { IAuthState } from "@/types";
import { RootState } from "@/redux/store";


const INITIAL_STATE: IAuthState = {
}

const authSlice = createSlice({
  name: "auth",
  initialState: INITIAL_STATE,
  reducers: {

    setAuthState: (state, action: PayloadAction<IAuthState>) => {
      console.log("payload=", action.payload);
      state.user = action.payload.user;
      state.accessToken = action.payload.accessToken;
    },
    removeAuthState: (state) => {
      state.user = undefined;
      state.accessToken = undefined;
    }

  }
})


export default authSlice.reducer;
export const { setAuthState, removeAuthState } = authSlice.actions;
export const selectAuthState = (state: RootState) => state.auth;