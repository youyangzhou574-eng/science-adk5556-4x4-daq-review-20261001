def verify_template(t,pos,old):
 rr=t['refs'];kind=t['kind'];tol=1e-8
 eq=lambda a,b:abs(a-b)<tol
 rot=lambda:all(eq(pos[r][2],t['rotation'])for r in rr)
 if kind=='EQUAL_PITCH_ROW':
  ax=0 if t['axis']=='x'else 1;other=1-ax
  return rot()and all(eq(pos[r][other],pos[rr[0]][other])for r in rr)and all(eq(pos[rr[i+1]][ax]-pos[rr[i]][ax],t['pitchMm'])for i in range(len(rr)-1))
 if kind=='PIN_FACING_MIRROR_2_PLUS_2':
  if len(rr)!=4:return False
  a,b,c,d=[pos[r]for r in rr]
  return rot()and eq(a[1],b[1])and eq(c[1],d[1])and eq(a[0],d[0])and eq(b[0],c[0])and eq(b[0]-a[0],t['pitchXmm'])and eq(c[1]-b[1],t['pitchYmm'])
 if kind=='FOUR_CHANNEL_TWO_ROW':
  if len(rr)!=8:return False
  a,b=rr[:4],rr[4:]
  return rot()and all(eq(pos[a[i]][0],pos[b[i]][0])for i in range(4))and all(eq(pos[a[i+1]][0]-pos[a[i]][0],t['pitchXmm'])for i in range(3))and all(eq(pos[r][1],pos[a[0]][1])for r in a)and all(eq(pos[r][1],pos[b[0]][1])for r in b)and eq(pos[a[0]][1]-pos[b[0]][1],t['pitchYmm'])
 if kind=='CENTRAL_POSITIONAL_MIRROR':
  if len(rr)!=2:return False
  a,b=[pos[r]for r in rr];x,y=t['axisCenter']
  return rot()and eq((a[0]+b[0])/2,x)and eq((a[1]+b[1])/2,y)
 if kind=='PIN_FORCED_BASELINE':
  return all(tuple(pos[r])==tuple(old[r])for r in rr)
 return False

