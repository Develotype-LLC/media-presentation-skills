import React from 'react';
import {AbsoluteFill, Composition, interpolate, registerRoot, useCurrentFrame} from 'remotion';
const beats = [
 {title:'Start with the message.',body:'What should the audience understand or do?'},
 {title:'Make the choice visible.',body:'Use a scene that explains the idea.'},
 {title:'Keep the story editable.',body:'Footage, narration, and labels stay separate.'},
];
const Story = () => {
 const frame=useCurrentFrame(); const index=Math.min(2,Math.floor(frame/96));
 const opacity=interpolate(frame%96,[0,12,84,95],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 return <AbsoluteFill style={{background:'#101c2d',color:'#f6f4ef',fontFamily:'Arial',justifyContent:'center',padding:90}}>
  <div style={{opacity}}><div style={{color:'#70d9d0',fontSize:24}}>MEDIA STORY LAB</div><h1 style={{fontSize:64}}>{beats[index].title}</h1><p style={{fontSize:30}}>{beats[index].body}</p></div>
 </AbsoluteFill>;
};
registerRoot(()=> <Composition id="Story" component={Story} durationInFrames={288} fps={24} width={1280} height={720}/>);
