import test from 'node:test'
import assert from 'node:assert/strict'
import { buildRoutine } from './frontend/src/utils/recommendations.js'
const product = (id, category, type, concern, stock=5) => ({id,category,skin_type:[type],skin_concern:[concern],name:concern,stock})
const catalog = [product(1,'cleansers','Dry','Hydration'),product(2,'cleansers','Oily','Breakouts'),product(3,'moisturizers','Dry','Hydration'),product(4,'moisturizers','Oily','Breakouts'),product(5,'sunscreens','All Skin Types','Protection'),product(6,'serums','Dry','Hydration'),product(7,'serums','Dry','Brighter Tone'),product(8,'toners','Dry','Hydration'),product(9,'serums','Dry','Hydration',0)]
const profile = {skinType:'Dry',goals:['Hydration'],concerns:[],routineLevel:'Essential (3-4 Steps)'}
test('skin type changes recommended catalog IDs',()=>assert.notDeepEqual(buildRoutine(catalog,profile).map(p=>p.id),buildRoutine(catalog,{...profile,skinType:'Oily'}).map(p=>p.id)))
test('goals rank treatment candidates',()=>{assert.equal(buildRoutine(catalog,profile).find(p=>p.category==='serums').id,6);assert.equal(buildRoutine(catalog,{...profile,goals:['Brighter Tone']}).find(p=>p.category==='serums').id,7)})
test('minimal evening is two steps without sunscreen',()=>{const routine=buildRoutine(catalog,{...profile,routineLevel:'Minimal (2 Steps)'},true);assert.equal(routine.length,2);assert.ok(routine.every(p=>p.category!=='sunscreens'))})
test('complete morning uses five distinct in-stock products',()=>{const routine=buildRoutine(catalog,{...profile,routineLevel:'Complete (5 Steps)'});assert.equal(routine.length,5);assert.equal(new Set(routine.map(p=>p.id)).size,5);assert.ok(routine.every(p=>p.stock>0))})
test('empty catalog never fabricates a recommendation',()=>assert.deepEqual(buildRoutine([],profile),[]))
