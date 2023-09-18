// + All types used in the react app

export interface IUser {
  username: string;
}

export interface IAuthState {
  user?: IUser;
  accessToken?: string;
}
