import { apiSlice } from "@/app/api/apiSlice";


interface ILoginDetails {
  username: string;
  plainPassword: string;
}


export const authApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({

    login: builder.mutation({
      query: (credentials: ILoginDetails) => ({
        url: '/auth',
        method: 'POST',
        body: { ...credentials }
      })
    }),

  })
})

export const { useLoginMutation } = authApiSlice