import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, LoginFormValues } from "@/schemas/login.schema";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import { Link } from "react-router-dom";
import { CgProfile } from "react-icons/cg";

const LoginForm = () => {
  const [showPassword, setShowPassword] = useState(false);

  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onsubmit = (data: LoginFormValues) => {
    console.log("Form Data: ", data);
  };

  return (
    <div className="w-96 mx-auto p-6 rounded-2xl shadow-md bg-white dark:bg-zinc-900">
      <div className="flex flex-col gap-2 items-center mb-4">
        <CgProfile size={56} />
        <h1 className="text-3xl font-serif italic font-semibold mb-4 text-center">
          Login
        </h1>
      </div>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onsubmit)} className="space-y-2">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input placeholder="john@example.com" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <div className="relative">
                    <Input
                      type={showPassword ? "text" : "password"}
                      placeholder="********"
                      {...field}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword((prev) => !prev)}
                      className="absolute right-2 top-2 text-muted-foreground"
                    >
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <div className="w-full text-end">
            <Link
              to={"/forgot-password"}
              className="text-sm hover:text-red-500 hover:underline"
            >
              Forgot Password
            </Link>
          </div>
          <div className="pt-4">
            <Button type="submit" className="w-full">
              Login
            </Button>
          </div>
        </form>
      </Form>
      <p className="text-sm text-center mt-4">
        Don't have an account?{" "}
        <Link
          to={"/signup"}
          className="text-red-500 font-semibold hover:underline"
        >
          Signup
        </Link>{" "}
      </p>
    </div>
  );
};

export default LoginForm;
