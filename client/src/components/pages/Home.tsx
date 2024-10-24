import VideoStream from "../video/Video";
import { Avatar } from "@nextui-org/avatar";
export default function Home() {
  return (
    <section className="Home p-2 flex items-center" id="Home">
      <div className=" flex flex-wrap ">
        <div className=" flex-[3_0_540px]" id="Video">
          <VideoStream />
        </div>
        <div
          className=" flex-[1_0_340px] border flex flex-col p-4 items-center justify-center"
          id="User"
        >
          <Avatar
            isBordered
            src="https://i.pravatar.cc/150?u=a042581f4e29026024d"
            className="w-44 h-44 text-large"
            radius="lg"
          />
          <br />
          <h2>ID: 64028780</h2>
          <h2>NAME: Phonsing Taleman</h2>
          <h2>TIME: Thu 17 Oct 2024 14:48</h2>
        </div>
      </div>
    </section>
  );
}
