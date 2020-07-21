'use strict'

const states = require('./data.json')
const trades = require('./output.json')

const [balanceA, balanceB] = [{ cash: 0, position: 0 }, { cash: 0, position: 0 }]

let lastTrade

while (trades.length) {
  let { time, actions } = trades.shift()
  if (time < lastTrade + 30 * 1000) throw new Error(`invalid trade! Wait at least 30 seconds between trades... (${time - lastTrade})`)
  lastTrade = time

  const { assetA: { ask: askA, bid: bidA }, assetB: { ask: askB, bid: bidB } } = states[time]

  if (actions.includes('buyA')) {
    balanceA.position += 1
    balanceA.cash -= askA
  }
  if (actions.includes('sellB')) {
    balanceB.position -= 1
    balanceB.cash += bidB
  }
  if (actions.includes('sellA')) {
    balanceA.position -= 1
    balanceA.cash += bidA
  }
  if (actions.includes('buyB')) {
    balanceB.position += 1
    balanceB.cash -= askB
  }

  const a_pnl = balanceA.cash + balanceA.position * (balanceA.position > 0 ? bidA : askA)
  const b_pnl = balanceB.cash + balanceB.position * (balanceB.position > 0 ? bidB : askB)

  console.log(`${time}: ${a_pnl} + ${b_pnl} = ${a_pnl + b_pnl}`)
}

