import SingleTrick from "./SingleTrick";
function LevelTricks({ level }) {
  return (
    <div>
      {level}
      <SingleTrick name="Back Flip" />
    </div>
  );
}
export default LevelTricks
