import React, { useState } from "react";
import { Button, Modal, Upload, message } from "antd";
import type { UploadFile, UploadProps } from "antd";
import { Image } from "@nextui-org/react";
import axios from "axios";

const NewUser: React.FC = () => {
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [previewVisible, setPreviewVisible] = useState(false);
  const [previewImage, setPreviewImage] = useState<string | null>(null);
  const [messageApi, contextHolder] = message.useMessage();

  const onChange: UploadProps["onChange"] = ({ fileList: newFileList }) => {
    setFileList(newFileList);
  };

  const handlePreview = async (file: UploadFile) => {
    let src = file.url as string;
    if (!src && file.originFileObj) {
      src = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.readAsDataURL(file.originFileObj as Blob);
        reader.onload = () => resolve(reader.result as string);
      });
    }
    setPreviewImage(src);
    setPreviewVisible(true);
  };

  const handleUpload = async () => {
    //console.log(fileList);
    const formData = new FormData();
    fileList.forEach((file) => {
      if (file.originFileObj) {
        //console.log(file.originFileObj);
        formData.append("images", file.originFileObj); // Use originFileObj for upload
      }
    });
    try {
      const response = await axios.post(
        "http://localhost:3000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      if (response.status === 201) {
        messageApi.open({
          type: "success",
          content: "Image uploaded successfully!",
        });
        setFileList([]);
      }
    } catch (error) {
      messageApi.open({
        type: "error",
        content: "Failed to upload image.",
      });
      console.error(error); // Log the error for debugging
    }
  };

  return (
    <>
      {contextHolder}
      <Upload
        listType="picture-card"
        fileList={fileList}
        multiple={true}
        onChange={onChange}
        onPreview={handlePreview}
        beforeUpload={() => false}
      >
        {fileList.length < 5 && "+ Upload"}
      </Upload>
      <Modal
        open={previewVisible}
        title="Image Preview"
        footer={null}
        onCancel={() => setPreviewVisible(false)}
        className="flex justify-center items-center"
      >
        <Image alt="Cropped Preview" isZoomed src={previewImage || ""} />
      </Modal>
      <Button
        type="primary"
        onClick={handleUpload}
        disabled={fileList.length === 0}
        style={{ marginTop: 16 }}
      >
        Upload Cropped Image
      </Button>
    </>
  );
};

export default NewUser;
