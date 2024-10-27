import { Table } from "antd";
import { Avatar, AvatarGroup, Button } from "@nextui-org/react";
import type { TableProps } from "antd";
import { MdEditSquare } from "react-icons/md";

import { data } from "../table/data";
//mport NewUser from "../form/NewUser";
interface DataType {
  key: string;
  name: string;
  money: string;
  address: string;
}
const columns: TableProps<DataType>["columns"] = [
  {
    title: "Name",
    dataIndex: "name",
    render: (text) => <a>{text}</a>,
  },
  {
    title: "Images",
    dataIndex: "money",
    render: () => (
      <AvatarGroup isBordered>
        <Avatar src="https://i.pravatar.cc/150?u=a042581f4e29026024d" />
        <Avatar src="https://i.pravatar.cc/150?u=a04258a2462d826712d" />
        <Avatar src="https://i.pravatar.cc/150?u=a042581f4e29026704d" />
        <Avatar src="https://i.pravatar.cc/150?u=a04258114e29026302d" />
        <Avatar src="https://i.pravatar.cc/150?u=a04258114e29026702d" />
        <Avatar src="https://i.pravatar.cc/150?u=a04258114e29026708c" />
      </AvatarGroup>
    ),
  },
  {
    title: "Introduction",
    dataIndex: "address",
  },
  {
    title: "Action",
    className: "w-32",
    render: () => (
      <Button
        color="primary"
        size="sm"
        radius="sm"
        variant="light"
        startContent={<MdEditSquare size={20} className="text-default-500" />}
      >
        Edit
      </Button>
    ),
  },
];

function New() {
  return (
    <section className="py-10 px-4 " id="Home">
      <h2 className="text-3xl">Employess</h2>
      <br />
      <div id="video" className="">
        <div className="mx-auto max-w-full">
          <Table<DataType>
            columns={columns}
            dataSource={data}
            bordered
            title={() => "Header"}
            footer={() => "Footer"}
          />
          {/* <NewUser/> */}
        </div>
      </div>
    </section>
  );
}

export default New;
