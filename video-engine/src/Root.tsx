import { Composition } from "remotion";
import { FORMATS } from "./lib/formats";
import { CNReel, reelDuration } from "./cn/CNReel";
import { REELS } from "./cn/reels51";
import { CNCover } from "./cn/CNCover";
import { Quad4, QUAD_FRAMES } from "./cn/Quad4";
import { CNLong, longDuration } from "./cn/CNLong";
import { LONGS } from "./cn/long";
import { RSReel, rsDuration } from "./rs/RSReel";
import rsDemo from "./rs/demo.json";

const reel = FORMATS.reel;

export const RemotionRoot: React.FC = () => (
  <>
    {REELS.map((r) => (
      <Composition key={r.id} id={r.id} component={CNReel} durationInFrames={reelDuration(r.props)} {...reel} defaultProps={r.props} />
    ))}
    {/* copertine: stesso formato per tutti i reel che hanno `cover` (id del reel + «-copertina»). Composition a 30 fps e non Still (che va a 1 fps): così `frame` è il fotogramma del master */}
    {REELS.filter((r) => r.cover).map((r) => (

      <Composition key={`${r.id}-copertina`} id={`${r.id}-copertina`} component={CNCover} width={1080} height={1920} fps={30} durationInFrames={1} defaultProps={{ ...r.cover!, master: (r.cover!.master ?? r.props.master).replace("_fx.mp4", ".mp4").replace("C6-metronomo-manuale", "C6-metronomo"), frame: r.cover!.frame ?? 60 }} />
    ))}
    {/* G13 · reel veloce a schermo diviso in quattro (i quattro esercizi del circuito, muti) con banner della guida */}
    <Composition id="G13-quattro" component={Quad4} durationInFrames={QUAD_FRAMES} {...reel} defaultProps={{ kicker: "Prima di correre al freddo", title: ["4 esercizi", "per scaldarti in casa"], guide: ["Guida gratuita: come scaldarsi", "quando fa freddo"], word: "CIRCUITO" }} />
    <Composition id="G13-quattro-copertina" component={CNCover} width={1080} height={1920} fps={30} durationInFrames={1} defaultProps={{ master: "ytcn26/masters/G4-casa.mp4", frame: 868, kicker: "Correre al freddo", lines: ["4 esercizi per", "scaldarti in casa"], accent: "scaldarti in casa" }} />
    {LONGS.map((r) => (
      <Composition key={r.id} id={r.id} component={CNLong} durationInFrames={longDuration(r.props)} width={1920} height={1080} fps={30} defaultProps={r.props} />
    ))}
    {/* Motore ReelStudio (project.json del PC): props = scripts/rs_props.ts */}
    <Composition
      id="RSReel"
      component={RSReel}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={150}
      defaultProps={rsDemo as any}
      calculateMetadata={({ props }: any) => ({ durationInFrames: rsDuration(props), fps: props.fps || 30 })}
    />
  </>
);
