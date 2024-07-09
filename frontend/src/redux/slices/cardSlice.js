import { createSlice } from '@reduxjs/toolkit';

const cardSlice = createSlice({
  name: 'cards',
  initialState: { items: [] },
  reducers: {
    setCards: (state, action) => {
      state.items = action.payload;
    },
  },
});

export const { setCards } = cardSlice.actions;
export default cardSlice.reducer;
